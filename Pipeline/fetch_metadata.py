import importlib.util
import json
import os
import urllib.request
from datetime import datetime
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCAL_PDB_DIR = ROOT / "Fetch-AA-info" / "PDB-Database"
RCSB_GRAPHQL_URL = "https://data.rcsb.org/graphql"
RCSB_BATCH_SIZE = 100

RCSB_QUERY = """
query($ids: [String!]!) {
  entries(entry_ids: $ids) {
    rcsb_id
    rcsb_accession_info { deposit_date }
    polymer_entities {
      rcsb_polymer_entity { pdbx_description }
      rcsb_polymer_entity_container_identifiers { auth_asym_ids }
      rcsb_entity_source_organism { scientific_name source_type }
    }
  }
}
"""


@lru_cache(maxsize=None)
def _load_pdb_file_parser():
    # reuse the PDB file parsing of Fetch-AA-info/Fetcher_2.py (folder name is not importable)
    spec = importlib.util.spec_from_file_location("Fetcher_2", ROOT / "Fetch-AA-info" / "Fetcher_2.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def metadata_from_pdb_file(pdb_file_path):
    # read protein names, engineered flags, date and organism from a local PDB file
    fetcher = _load_pdb_file_parser()
    protein_names, engineered = fetcher.extract_protein_info_from_compnd(pdb_file_path)
    organism = fetcher.extract_organism(pdb_file_path)
    chains = {chain: {"Protein Name": name, "Engineered": engineered.get(chain, "NO"), "Organism": organism}
              for chain, name in protein_names.items()}
    return {"Founded Date": fetcher.extract_founded_date_from_header(pdb_file_path), "chains": chains}


def metadata_from_rcsb_entry(entry):
    # convert one RCSB GraphQL entry into the same shape as metadata_from_pdb_file
    deposit_date = (entry.get("rcsb_accession_info") or {}).get("deposit_date")
    founded_date = "N/A"
    if deposit_date:
        # same format as the PDB HEADER line (e.g. 14-APR-97), expected by DatabaseGenerator
        founded_date = datetime.strptime(deposit_date[:10], "%Y-%m-%d").strftime("%d-%b-%y").upper()

    chains = {}
    for entity in entry.get("polymer_entities") or []:
        name = ((entity.get("rcsb_polymer_entity") or {}).get("pdbx_description") or "N/A").upper()
        sources = entity.get("rcsb_entity_source_organism") or []
        organism = (sources[0].get("scientific_name") or "N/A").upper() if sources else "N/A"
        engineered = "YES" if sources and "genetically" in (sources[0].get("source_type") or "") else "NO"
        for chain in (entity.get("rcsb_polymer_entity_container_identifiers") or {}).get("auth_asym_ids") or []:
            chains[chain] = {"Protein Name": name, "Engineered": engineered, "Organism": organism}
    return {"Founded Date": founded_date, "chains": chains}


def query_rcsb(pdb_ids):
    # fetch metadata for several PDB entries with one GraphQL request
    body = json.dumps({"query": RCSB_QUERY, "variables": {"ids": pdb_ids}}).encode()
    request = urllib.request.Request(RCSB_GRAPHQL_URL, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(request, timeout=60) as response:
        result = json.load(response)
    entries = (result.get("data") or {}).get("entries") or []
    return {entry["rcsb_id"].upper(): metadata_from_rcsb_entry(entry) for entry in entries}


def fetch_metadata(chains_by_id, cache_path=None, offline=False, pdb_dir=LOCAL_PDB_DIR, log=print):
    """Return {pdb_id: {"Founded Date": ..., "chains": {chain: {...}}}} for {pdb_id: [chain, ...]}.

    Local PDB files (pdb<id>.ent) are used first, then the RCSB API; API results are cached in cache_path.
    IDs that cannot be found are missing from the result.
    """
    cache = {}
    if cache_path and os.path.exists(cache_path):
        with open(cache_path, "r") as cache_file:
            cache = json.load(cache_file)

    metadata = {}
    incomplete_local = {}  # local files without names for all requested chains (e.g. wrapped MOLECULE lines)
    missing = []
    for pdb_id, chains in sorted(chains_by_id.items()):
        pdb_file_path = Path(pdb_dir) / f"pdb{pdb_id.lower()}.ent"
        local = metadata_from_pdb_file(pdb_file_path) if pdb_file_path.exists() else None
        if local and all((local["chains"].get(chain) or {}).get("Protein Name") for chain in chains):
            metadata[pdb_id] = local
            continue
        if local:
            incomplete_local[pdb_id] = local
        if pdb_id in cache:
            metadata[pdb_id] = cache[pdb_id]
        else:
            missing.append(pdb_id)

    if missing and offline:
        log(f"Offline: no metadata for {len(missing)} PDB IDs")
    elif missing:
        log(f"Fetching metadata for {len(missing)} PDB IDs from RCSB")
        for start in range(0, len(missing), RCSB_BATCH_SIZE):
            fetched = query_rcsb(missing[start:start + RCSB_BATCH_SIZE])
            metadata.update(fetched)
            cache.update(fetched)
        if cache_path:
            os.makedirs(os.path.dirname(cache_path), exist_ok=True)
            with open(cache_path, "w") as cache_file:
                json.dump(cache, cache_file, indent=1)
        not_found = [pdb_id for pdb_id in missing if pdb_id not in metadata]
        if not_found:
            log(f"RCSB has no entry for: {', '.join(not_found)}")

    # fall back to the partly read local files where RCSB did not help
    for pdb_id, local in incomplete_local.items():
        metadata.setdefault(pdb_id, local)
    return metadata
