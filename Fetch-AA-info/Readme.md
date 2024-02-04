
# PDB Data Fetcher

This Python script, `PDB-FETCH.py`, is designed to download PDB (Protein Data Bank) files for protein sequences specified in a FASTA file.

## Requirements

To run this script, ensure you have the following dependencies installed:

- Biopython

# PDB Data Fetcher

This Python script, `PDB-FETCH.py`, is designed to download PDB (Protein Data Bank) files for each sequence ID specified in an input FASTA file. The downloaded PDB files will be saved in a folder named `PDB-Database`, which is created automatically if it doesn't exist.

## Functions

### `download_pdb_file(pdb_id, output_folder="PDB-Database")`

This function downloads a PDB file for a given PDB ID and saves it to the specified output folder. If no output folder is provided, it defaults to `PDB-Database`.

## Example

An example of running the script:

```bash
python PDB-FETCH.py
```


I have removed all the additional information in the Seq ID to fetch the protein informations
