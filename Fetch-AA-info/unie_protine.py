import json
import csv

def count_unique_protein_names(json_file_path):
    protein_name_count = {}

    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

        # Assuming 'Protein Name' is the key containing the protein names
        for entry in data:
            protein_name = entry.get('Protein Name')
            if protein_name:
                protein_name_count[protein_name] = protein_name_count.get(protein_name, 0) + 1

    return protein_name_count

def export_to_tsv(protein_name_count, tsv_filename):
    # Export data to a TSV file
    with open(tsv_filename, 'w', newline='') as tsv_file:
        writer = csv.writer(tsv_file, delimiter='\t')

        # Write the header
        writer.writerow(['Protein Name', 'Count'])

        # Write the data rows
        for protein_name, count in protein_name_count.items():
            writer.writerow([protein_name, count])

# Replace 'your_file.json' with the actual path to your JSON file
json_file_path = 'output_data.json'
tsv_filename = 'output_unique_proteins.tsv'

protein_name_count = count_unique_protein_names(json_file_path)
export_to_tsv(protein_name_count, tsv_filename)

print(f"Data exported to {tsv_filename}")