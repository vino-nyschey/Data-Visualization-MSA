from collections import Counter

from Bio import Align
from Bio.Align import substitution_matrices


def _make_aligner():
    # global protein alignment, free end gaps so short fragments (e.g. peptides) are not penalised
    aligner = Align.PairwiseAligner(mode="global",
                                    substitution_matrix=substitution_matrices.load("BLOSUM62"),
                                    open_gap_score=-10, extend_gap_score=-0.5)
    aligner.end_gap_score = 0
    return aligner


def _kmers(sequence, k=3):
    return Counter(sequence[i:i + k] for i in range(len(sequence) - k + 1))


def choose_center(sequences):
    # index of the sequence sharing the most 3-mers with all others (cheap stand-in for pairwise scores)
    kmers = [_kmers(seq) for seq in sequences]
    best_index, best_score = 0, -1
    for i, own in enumerate(kmers):
        score = sum(sum((own & other).values()) for j, other in enumerate(kmers) if j != i)
        if score > best_score:
            best_index, best_score = i, score
    return best_index


def align_sequences(records):
    """Multiple sequence alignment of [(sequence_id, sequence), ...] with the center-star method.

    Every sequence is aligned pairwise to the most central sequence; the gaps of all pairwise
    alignments are then merged into one alignment. Returns [(sequence_id, aligned_sequence), ...]
    in the input order.
    """
    if len(records) < 2:
        return list(records)

    aligner = _make_aligner()
    alphabet = set(aligner.substitution_matrix.alphabet)
    # letters missing from BLOSUM62 (e.g. U, O) are aligned as X but written back unchanged
    sanitized = ["".join(aa if aa in alphabet else "X" for aa in seq.upper()) for _, seq in records]
    center_index = choose_center(sanitized)
    center = sanitized[center_index]
    center_length = len(center)

    # per sequence: residues inserted before each center position, and the residue aligned to it
    insertions, matches = [], []
    for index, (_, sequence) in enumerate(records):
        inserted = [""] * (center_length + 1)
        matched = ["-"] * center_length
        if index == center_index:
            matched = list(sequence)
        else:
            alignment = aligner.align(center, sanitized[index])[0]
            i = j = 0  # positions in center and in this sequence
            for center_char, other_char in zip(alignment[0], alignment[1]):
                residue = sequence[j] if other_char != "-" else "-"
                if other_char != "-":
                    j += 1
                if center_char == "-":
                    inserted[i] += residue
                else:
                    matched[i] = residue
                    i += 1
        insertions.append(inserted)
        matches.append(matched)

    # widest insertion at each center position over all sequences
    widths = [max(len(inserted[i]) for inserted in insertions) for i in range(center_length + 1)]

    aligned = []
    for (sequence_id, _), inserted, matched in zip(records, insertions, matches):
        parts = []
        for i in range(center_length + 1):
            parts.append(inserted[i].ljust(widths[i], "-"))
            if i < center_length:
                parts.append(matched[i])
        aligned.append((sequence_id, "".join(parts)))
    return aligned
