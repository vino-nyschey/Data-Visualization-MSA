import json
import os
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent

# dataset built from an uploaded FASTA file (see Pipeline/build_dataset.py)
ACTIVE_DIR = ROOT / "datasets" / "active"
# bundled sample dataset (protein_sequence_analysis_lpt.fasta)
SAMPLE_DATABASE = ROOT / "Database" / "ProteinDatabase.json"
SAMPLE_MSA_DIR = ROOT / "MSA_FLASK" / "fasta_files" / "MSA_align_files"


def using_uploaded_dataset():
    return (ACTIVE_DIR / "ProteinDatabase.json").exists()


def database_path():
    return ACTIVE_DIR / "ProteinDatabase.json" if using_uploaded_dataset() else SAMPLE_DATABASE


def msa_dir():
    return ACTIVE_DIR / "MSA_align_files" if using_uploaded_dataset() else SAMPLE_MSA_DIR


_cache = {}


def load_protein_data():
    # list of protein entries of the current dataset, re-read only when the file changes
    path = database_path()
    if not path.exists():
        return []
    key = (path, os.path.getmtime(path))
    if key not in _cache:
        with open(path, "r") as json_file:
            _cache.clear()
            _cache[key] = json.load(json_file)
    return _cache[key]


def load_protein_dataframe():
    return pd.json_normalize(load_protein_data())


def one_chain_per_protein(data):
    # keep one row per PDB entry (chain A if present, otherwise its first chain)
    chains = data['Sequence ID'].str.split(':').str[1]
    ordered = data.assign(_not_chain_a=chains != 'A').sort_values('_not_chain_a', kind='stable')
    return ordered.drop_duplicates('PDB ID').sort_index().drop(columns='_not_chain_a')
