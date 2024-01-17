import json
import csv
import re

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

def cluster_and_count_proteins(json_file_path):
    protein_clusters = {}

    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

        # Assuming 'Protein Name' is the key containing the protein names
        for entry in data:
            protein_name = entry.get('Protein Name')
            if protein_name:
                # Handle specific cases for "ACYL-HYDROLASE" and "S-TRANSFERASE"
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
                else:
                    # Extract a word containing "ase" or "peptide" from 'Protein Name'
                    ase_word = extract_ase_word(protein_name)

                # If a valid "ase" or "peptide" word is found, use it as the cluster key
                cluster_key = ase_word if ase_word else "OTHER"

                # Update the protein_clusters dictionary
                if cluster_key not in protein_clusters:
                    protein_clusters[cluster_key] = {'Protein Names': [], 'Count': 0}

                protein_clusters[cluster_key]['Protein Names'].append(protein_name)
                protein_clusters[cluster_key]['Count'] += 1

    # Check and move protein families with count less than 5 to "OTHER"
    for cluster_key, values in list(protein_clusters.items()):
        if values['Count'] < 5:
            protein_clusters['OTHER']['Protein Names'].extend(values['Protein Names'])
            protein_clusters['OTHER']['Count'] += values['Count']
            del protein_clusters[cluster_key]

    return protein_clusters


def export_to_tsv(protein_clusters, tsv_filename):
    # Export data to a TSV file
    with open(tsv_filename, 'w', newline='') as tsv_file:
        writer = csv.writer(tsv_file, delimiter='\t')

        # Write the header
        writer.writerow(['Protein Family', 'Protein Name', 'Count'])

        # Write the data rows
        for cluster_key, values in sorted(protein_clusters.items()):
            for protein_name in values['Protein Names']:
                writer.writerow([cluster_key, protein_name, values['Count']])

# Replace 'your_file.json' with the actual path to your JSON file
json_file_path = 'output_data.json'
tsv_filename = 'output_protein_clusters.tsv'

protein_clusters = cluster_and_count_proteins(json_file_path)
export_to_tsv(protein_clusters, tsv_filename)

print(f"Data exported to {tsv_filename}")
