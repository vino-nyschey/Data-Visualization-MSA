import json
import csv
import collections
import os

# Replace 'added_protein_cluster.json' with the actual path to your JSON file
input_json_path = 'ProteinDatabase.json'
output_tsv_folder = 'ProtineOverview/'

# Load existing data from JSON file
with open(input_json_path, 'r') as json_file:
    existing_data = json.load(json_file)

# Define the categories to count
categories_to_count = ["PDB ID", "Protein Name", "Organism", "Engineered", "Sequence Length", "Protein Family", "No. of Chains", "Discovered Year"]

# Create a folder to save TSV files
os.makedirs(output_tsv_folder, exist_ok=True)

# Count unique values for each category and save to a separate TSV file
for category in categories_to_count:
    category_counts = collections.Counter(entry.get(category) for entry in existing_data)
    total_count = sum(category_counts.values())  # Calculate the total count for the category
    output_tsv_path = os.path.join(output_tsv_folder, f'counts_of_{category}.tsv')
    with open(output_tsv_path, 'w', newline='', encoding='utf-8') as tsv_file:
        tsv_writer = csv.writer(tsv_file, delimiter='\t')
        tsv_writer.writerow([category, 'Value', 'Count'])  # Modify the header to include 'Value' column
        for value, count in category_counts.items():
            tsv_writer.writerow([value, count])
        tsv_writer.writerow(['Total', total_count])  # Add a row for the total count

    print(f"Unique counts for category '{category}' exported to {output_tsv_path}")
