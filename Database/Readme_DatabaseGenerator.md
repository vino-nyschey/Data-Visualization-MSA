## Functions

### `clean_ase_word(word)`

This function removes prefixes ending with "-" and suffixes starting with "," from a given word. It is primarily used to clean up words containing the suffix "ase" or "peptide".

### `extract_ase_word(protein_name)`

This function extracts a word containing "ase" or "peptide" from a protein name. It splits the protein name into words and selects the first word containing "ase" or "peptide". If none is found, it returns None.

### `add_protein_family_info(data)`

This function adds protein family information to each entry in the data. It identifies protein family names based on specific cases or by extracting words containing "ase" or "peptide" from the protein names.

### `add_chain_count(data)`

This function adds chain count information to each entry in the data. It counts the occurrences of each PDB ID and assigns the count to the corresponding entries.

### `convert_founded_date_to_year(data)`

This function converts the founded date to discovered year and removes the founded date entry from each entry in the data. It extracts the year from the founded date and updates the entry accordingly.

### `cluster_organism(data)`

This function clusters organism names based on species. It cleans and standardizes organism names, replaces specific keywords with desired labels, and clusters less frequent organisms into an "OTHER SP." category.


`ProteinOverview.py`, `TestDatabase.py` for test the database clusters.

Purpose, to cluster the Organism and Protein after data manipulation