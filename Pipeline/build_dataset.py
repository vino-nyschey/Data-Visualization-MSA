"""Build a complete dataset for the website from a FASTA file of PDB chains.

Accepted headers: '>1AH7:A', '>1AH7:A|PDBID|CHAIN|SEQUENCE' (legacy RCSB format), '>1AH7_A' or
'>4HHB_1|Chains A, C|...' (current RCSB download format; one entry per listed chain).

Usage:
    python -m Pipeline.build_dataset input.fasta [--out datasets/active] [--offline] [--msa-dir DIR]

The output folder contains ProteinDatabase.json, the uploaded input.fasta and one aligned
FASTA file per protein family in MSA_align_files/.
"""
import argparse
import json
import os
import re
import shutil
import time
from pathlib import Path

from Database.DatabaseGenerator import enrich_protein_data
from Pipeline.align import align_sequences
from Pipeline.fetch_metadata import fetch_metadata

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT_DIR = ROOT / "datasets" / "active"
RCSB_CACHE_PATH = ROOT / "datasets" / "rcsb_cache.json"

HEADER_PATTERN = re.compile(r"^>\s*([0-9][A-Za-z0-9]{3})[:_]([A-Za-z0-9]{1,4})(?:[\s|].*)?$")
ENTITY_HEADER_PATTERN = re.compile(r"^>\s*([0-9][A-Za-z0-9]{3})_\d+\|Chains? ([^|]+)")
CHAIN_PATTERN = re.compile(r"([A-Za-z0-9]+)(?:\[auth ([A-Za-z0-9]+)\])?")
SEQUENCE_PATTERN = re.compile(r"^[A-Za-z*-]+$")


class InputError(ValueError):
    pass


def parse_header(line):
    # (pdb_id, [chain, ...]) of a FASTA header line, or None if it is not a PDB chain header
    match = ENTITY_HEADER_PATTERN.match(line)
    if match:
        # 'Chains A, B[auth C]': use the author chain ID, as in the legacy format and PDB files
        chains = [auth or label for label, auth in CHAIN_PATTERN.findall(match.group(2))]
        return (match.group(1).upper(), chains) if chains else None
    match = HEADER_PATTERN.match(line)
    return (match.group(1).upper(), [match.group(2)]) if match else None


def parse_input_fasta(text):
    # parse FASTA text into [(pdb_id, chain, sequence), ...]; raise InputError with all problems found
    entries, errors, seen = [], [], set()
    header, lines = None, []
    skipping = False  # inside the sequence of an invalid header (already reported)

    def finish():
        if header is None:
            return
        line_no, pdb_id, chains = header
        sequence = "".join(lines).replace("*", "").replace("-", "").upper()
        for chain in chains:
            if not sequence:
                errors.append(f"line {line_no}: {pdb_id}:{chain} has no sequence")
            elif (pdb_id, chain) in seen:
                errors.append(f"line {line_no}: duplicate sequence ID {pdb_id}:{chain}")
            else:
                seen.add((pdb_id, chain))
                entries.append((pdb_id, chain, sequence))

    for line_no, raw_line in enumerate(text.splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith(">"):
            finish()
            parsed = parse_header(line)
            if parsed:
                header, lines, skipping = (line_no, *parsed), [], False
            else:
                header, lines, skipping = None, [], True
                errors.append(f"line {line_no}: header '{line[:40]}' is not in the form >PDBID:CHAIN")
        elif header is None:
            if not skipping:
                errors.append(f"line {line_no}: sequence without a header")
                skipping = True
        elif SEQUENCE_PATTERN.match(line):
            lines.append(line)
        else:
            errors.append(f"line {line_no}: invalid characters in sequence of {header[1]}:{header[2][0]}")
    finish()

    if not entries and not errors:
        errors.append("no sequences found")
    if errors:
        raise InputError("; ".join(errors[:10]) + (f" (and {len(errors) - 10} more)" if len(errors) > 10 else ""))
    return entries


def build_records(entries, metadata):
    # combine input sequences with metadata into the format of Database/fetched_data.json
    records = []
    for pdb_id, chain, sequence in entries:
        entry = metadata.get(pdb_id, {})
        chain_info = entry.get("chains", {}).get(chain, {})
        organism = chain_info.get("Organism", "N/A")
        records.append({
            "Sequence ID": f"{pdb_id}:{chain}",
            "PDB ID": pdb_id,
            "Protein Name": chain_info.get("Protein Name") or "N/A",
            "Founded Date": entry.get("Founded Date", "N/A"),
            "Organism": organism if organism and organism != "N/A" else "UNKNOWN",
            "Engineered": chain_info.get("Engineered", "NO"),
            "Sequence": sequence,
            "Sequence Length": len(sequence),
        })
    return records


def family_file_name(family):
    # file name used by the MSA page; the part before '_' is shown as family name
    return re.sub(r"[^A-Za-z0-9-]+", "-", family).strip("-").upper() + "_align.fasta"


def write_fasta(path, records, width=60):
    with open(path, "w") as fasta_file:
        for sequence_id, sequence in records:
            fasta_file.write(f">{sequence_id}\n")
            for start in range(0, len(sequence), width):
                fasta_file.write(sequence[start:start + width] + "\n")


def write_family_alignments(protein_data, msa_dir, log=print):
    # one MSA per protein family, aligned with the built-in center-star aligner
    families = {}
    for protein in protein_data:
        families.setdefault(protein["Protein Family"], []).append((protein["Sequence ID"], protein["Sequence"]))
    os.makedirs(msa_dir, exist_ok=True)
    for family, records in sorted(families.items()):
        log(f"Aligning {family} ({len(records)} sequences)")
        write_fasta(os.path.join(msa_dir, family_file_name(family)), align_sequences(records))


def _move_into_place(build_dir, out_dir, attempts=5):
    # rename the finished folder; on Windows virus scanners briefly lock new files, so retry and
    # copy as last resort
    for attempt in range(attempts):
        try:
            os.replace(build_dir, out_dir)
            return
        except PermissionError:
            time.sleep(0.5 * (attempt + 1))
    shutil.copytree(build_dir, out_dir)
    shutil.rmtree(build_dir, ignore_errors=True)


def build_dataset(fasta_text, out_dir=DEFAULT_OUT_DIR, offline=False, msa_dir=None, log=print):
    """Create ProteinDatabase.json and MSA files for fasta_text in out_dir (replacing its content).

    msa_dir: optional folder with pre-aligned FASTA files (e.g. from MUSCLE) used instead of the
    built-in aligner. Returns the protein data.
    """
    entries = parse_input_fasta(fasta_text)
    log(f"Read {len(entries)} sequences")

    chains_by_id = {}
    for pdb_id, chain, _ in entries:
        chains_by_id.setdefault(pdb_id, []).append(chain)
    metadata = fetch_metadata(chains_by_id, cache_path=RCSB_CACHE_PATH, offline=offline, log=log)
    protein_data = enrich_protein_data(build_records(entries, metadata))

    # build into a temporary folder first so a failed run keeps the previous dataset
    out_dir = Path(out_dir)
    build_dir = out_dir.with_name(out_dir.name + ".building")
    shutil.rmtree(build_dir, ignore_errors=True)
    os.makedirs(build_dir)
    with open(build_dir / "input.fasta", "w") as input_file:
        input_file.write(fasta_text)
    with open(build_dir / "ProteinDatabase.json", "w") as json_file:
        json.dump(protein_data, json_file, indent=2)
    if msa_dir:
        shutil.copytree(msa_dir, build_dir / "MSA_align_files")
    else:
        write_family_alignments(protein_data, build_dir / "MSA_align_files", log=log)

    shutil.rmtree(out_dir, ignore_errors=True)
    _move_into_place(build_dir, out_dir)
    log(f"Dataset written to {out_dir}")
    return protein_data


def main():
    parser = argparse.ArgumentParser(description="Build a protein dataset for the website from a FASTA file.")
    parser.add_argument("fasta", help="FASTA file with headers like >1AH7:A")
    parser.add_argument("--out", default=str(DEFAULT_OUT_DIR), help="output folder (default: datasets/active, used by the website)")
    parser.add_argument("--offline", action="store_true", help="only use local PDB files and the RCSB cache")
    parser.add_argument("--msa-dir", help="folder with pre-aligned FASTA files to use instead of the built-in aligner")
    args = parser.parse_args()

    with open(args.fasta, "r") as fasta_file:
        fasta_text = fasta_file.read()
    try:
        build_dataset(fasta_text, out_dir=args.out, offline=args.offline, msa_dir=args.msa_dir)
    except InputError as e:
        parser.exit(1, f"Invalid input: {e}\n")


if __name__ == "__main__":
    main()
