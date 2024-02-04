# Protein Data Fetcher

This Python script, `Fetcher.py`, is designed to fetch information about protein sequences from PDB (Protein Data Bank) files and export the retrieved data to a JSON file.

## Requirements

To run this script, ensure you have the following dependencies installed:

- Biopython
- Python 3.x

You can install Biopython using pip:

```bash
pip install biopython

```

## Usage

1. Ensure your protein sequence data is stored in a FASTA file named `input1.fasta`. Each sequence in the FASTA file should have a sequence ID in the format `PDB_ID:CHAIN_ID`, where `PDB_ID` is the Protein Data Bank ID and `CHAIN_ID` is the chain identifier.

2. Run the script by executing the following command in your terminal:

```bash
python Fetcher.py
```
The script will process each sequence in the input FASTA file, fetch relevant information from the corresponding PDB files, and export the retrieved data to a JSON file named `fetched_data.json`.

## Functions

### `extract_pdb_id_and_chain(sequence_id)`

This function extracts the PDB ID and chain identifier from a sequence ID in the format `PDB_ID:CHAIN_ID`.

### `extract_organism(pdb_file_path)`

This function extracts organism information from the SOURCE record in a PDB file.

### `extract_protein_info_from_compnd(pdb_file_path)`

This function extracts protein names and engineered information from the COMPND section of a PDB file.

### `extract_founded_date_from_header(pdb_file_path)`

This function extracts the founded date from the HEADER line of a PDB file.

### `find_pdb_file(pdb_id)`

This function searches for PDB files recursively within the current working directory.

### `fetch_protein_info(pdb_id, amino_acid_sequence)`

This function fetches protein information (protein name, founded date, organism, engineered status) from a PDB file.

### `export_to_json(data, json_filename)`

This function exports data to a JSON file.

Sequence ID: 1abc:A
PDB ID: 1abc
Protein Name: PROTEIN A
Founded Date: 01-JAN-2000
Organism: Homo sapiens
Engineered: YES
Sequence: ACGT...
Sequence Length: 100
----------------------------------------
Data exported to fetched_data.json
