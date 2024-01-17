import json
import csv
import re
import collections

def clean_ase_word(word):
    # Remove prefixes ending with "-" and suffixes starting with ","
    cleaned_word = re.sub(r'^[^a-zA-Z]*-|,[^a-zA-Z]*$', '', word)
    return cleaned_word.upper()

def extract_ase_word(protein_name):
    # Extract a word containing "ase" or "peptide" from 'Protein Name'
    words = protein_name.split()
    ase_words = [word for word in words if 'ase' in word.lower()]
    peptide_words = [word for word in words if 'peptide' in word.lower()]

    if ase_words:
        return clean_ase_word(ase_words[0])
    elif peptide_words:
        return "PEPTIDE"
    else:
        return None

def add_protein_family_info(data):
    for entry in data:
        protein_name = entry.get('Protein Name')
        if protein_name:
            # Handle specific cases"
            if "ACYL-HYDROLASE" in protein_name:
                ase_word = "HYDROLASE"
            elif "PHOSPHOFRUCTO-2-KINASE/" in protein_name:
                ase_word = "KINASE"
            elif "S-TRANSFERASE" in protein_name:
                ase_word = "TRANSFERASE"
            elif "MONOPHOSPHATASE" in protein_name:
                ase_word = "PHOSPHATASE"
            elif "CARBOXYLESTERASE" in protein_name:
                ase_word = "ESTERASE"
            elif "AMINOTRANSFERASE" in protein_name:
                ase_word = "TRANSFERASE"
            elif "PHOSPHOLIPASE" in protein_name:
                ase_word = "LIPASE"
            elif "PROTEIN-TYROSINE-PHOSPHATASE" in protein_name:
                ase_word = "PHOSPHATASE"
            else:
                # Extract a word containing "ase" or "peptide" from 'Protein Name'
                ase_word = extract_ase_word(protein_name)

            # If a valid "ase" or "peptide" word is found, add it to the entry
            if ase_word:
                entry['Protein Family'] = ase_word
            else:
                entry['Protein Family'] = "OTHER"
    
    return data

def add_chain_count(data):
    pdb_id_counts = collections.Counter(entry.get('PDB ID') for entry in data)

    for entry in data:
        pdb_id = entry.get('PDB ID')
        if pdb_id:
            entry['No. of Chains'] = pdb_id_counts[pdb_id]

    return data

def convert_founded_date_to_year(data):
    for entry in data:
        founded_date = entry.get('Founded Date')
        if founded_date:
            # Extract the year from the founded date and update the entry
            year_match = re.search(r'\d{2}-[A-Z]{3}-(\d{2})', founded_date)
            if year_match:
                year = year_match.group(1)
                entry['Discovered Year'] = "19" + year if int(year) > 60 else "20" + year
                del entry['Founded Date']  # Remove the "Founded Date" entry
            else:
                entry['Discovered Year'] = None
        else:
            entry['Discovered Year'] = None
    
    return data

# Replace 'output_data.json' with the actual path to your JSON file
input_json_path = 'fetched_data.json'
output_json_path = 'ProteinDatabase.json'

# Load existing data from JSON file
with open(input_json_path, 'r') as json_file:
    existing_data = json.load(json_file)

# Add protein family information to each entry
data_with_family = add_protein_family_info(existing_data)

# Add chain count information to each entry
data_with_chain_count = add_chain_count(data_with_family)

# Convert Founded Date to Discovered Year and remove Founded Date
data_with_discovered_year = convert_founded_date_to_year(data_with_chain_count)

# Save the updated data to a new JSON file
with open(output_json_path, 'w') as json_file:
    json.dump(data_with_discovered_year, json_file, indent=2)

print(f"Data with Protein Family, Chain Count, and Discovered Year information exported to {output_json_path}")
