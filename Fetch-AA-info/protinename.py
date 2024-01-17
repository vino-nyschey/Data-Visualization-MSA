import json
import csv

def extract_unique_protein_names_sorted(json_file_path):
    unique_protein_names = set()

    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

        # Assuming 'Protein Name' and 'Organism' are the keys containing the respective information
        for entry in data:
            protein_name = entry.get('Protein Name')
            organism = entry.get('Organism')
            
            if protein_name and organism:
                unique_protein_names.add((protein_name, organism))

    # Sort by organism, then by protein name within each organism
    sorted_protein_names = sorted(unique_protein_names, key=lambda x: (x[1], x[0]))

    return sorted_protein_names

def export_to_tsv(sorted_protein_names, tsv_filename):
    # Export data to a TSV file
    with open(tsv_filename, 'w', newline='') as tsv_file:
        writer = csv.writer(tsv_file, delimiter='\t')

        # Write the header
        writer.writerow(['Count', 'Protein Name', 'Organism'])

        # Write the data rows
        for count, (name, organism) in enumerate(sorted_protein_names, start=1):
            writer.writerow([count, name, organism])

# Replace 'your_file.json' with the actual path to your JSON file
json_file_path = 'output_data.json'
tsv_filename = 'protine_cluster.tsv'

sorted_protein_names = extract_unique_protein_names_sorted(json_file_path)
export_to_tsv(sorted_protein_names, tsv_filename)

print(f"Data exported to {tsv_filename}")
