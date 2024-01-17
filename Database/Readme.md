# Protein Database Processing

## Overview

This script processes protein database data retrieved from a JSON file. It performs various tasks such as adding protein family information, chain count information, and converting the founded date to discovered year.

## Usage

1. Ensure you have the required input data in a JSON file. Replace 'fetched_data.json' (organically added missing informations from fetching) with the actual path to your input JSON file.

2. You could Use the generated data for the further usages, if you make any changes in 'fetched_data.json' then please follow the steps :

2. Run the script by executing the following command in your terminal:

    ```bash
    python DatabaseGenerator.py
    ```


3. The script will generate a new JSON file named 'ProteinDatabase.json' containing the processed data.

4. Replace `DatabaseGenerator.py` with `TestDatabase.py` and `ProteinOverView.py` if you need the Overview of the protein for your Data Visualization needs.


## Description

### `clean_ase_word(word)`

This function removes prefixes ending with "-" and suffixes starting with "," from a given word, returning the cleaned word in uppercase.

### `extract_ase_word(protein_name)`

This function extracts a word containing "ase" or "peptide" from the 'Protein Name' field. It uses specific cases for some proteins and calls `clean_ase_word` for general cases.

### `add_protein_family_info(data)`

This function adds protein family information to each entry in the data. It utilizes the `extract_ase_word` function and handles specific cases for certain proteins.

### `add_chain_count(data)`

This function adds chain count information to each entry in the data based on the 'PDB ID' field.

### `convert_founded_date_to_year(data)`

This function converts the 'Founded Date' field to 'Discovered Year' and removes the 'Founded Date' field from each entry in the data.

### Main Execution

The script loads existing data from 'fetched_data.json', applies the functions in the specified order, and saves the processed data to 'ProteinDatabase.json'.

## Output

The processed data is saved in 'ProteinDatabase.json', containing additional information on protein family, chain count, and discovered year.
