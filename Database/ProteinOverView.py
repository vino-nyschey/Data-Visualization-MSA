import json
import csv
import os

# Replace 'added_protein_cluster.json' with the actual path to your JSON file
input_json_path = 'ProteinDatabase.json'
output_tsv_folder = 'ProtineOverview/'

# Load existing data from JSON file
with open(input_json_path, 'r') as json_file:
    existing_data = json.load(json_file)

# Specify the columns to include in the TSV table
columns_to_include = ["PDB ID", "Protein Name", "Protein Family", "Organism", "Engineered"]

# Create a folder to save the TSV file
os.makedirs(output_tsv_folder, exist_ok=True)
output_tsv_path = os.path.join(output_tsv_folder, 'ProteinList.tsv')

with open(output_tsv_path, 'w', newline='', encoding='utf-8') as tsv_file:
    tsv_writer = csv.writer(tsv_file, delimiter='\t')
    
    # Write header with selected columns
    tsv_writer.writerow(columns_to_include)

    # Write data for selected columns
    for entry in existing_data:
        row_data = [entry.get(column, '') for column in columns_to_include]
        tsv_writer.writerow(row_data)

print(f"Selected columns exported to {output_tsv_path}")
