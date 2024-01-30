import os
import json

# Read data from the JSON file
input_json_file = "ProteinDatabase.json"  # Replace with your actual JSON file path
with open(input_json_file, "r") as json_file:
    protein_data = json.load(json_file)

# Create a directory to store the FASTA files
output_directory = "fasta_files"
os.makedirs(output_directory, exist_ok=True)

# Create one FASTA file for each Protein Family
fasta_files = {}  # Dictionary to store FASTA content for each Protein Family

for protein in protein_data:
    family = protein["Protein Family"]
    sequence_id = protein["Sequence ID"]
    organism = protein["Organism"]
    protein_name = protein["Protein Name"]
    sequence = protein["Sequence"]

    # Include Organism and Protein Name in the FASTA content
    fasta_content = f">{sequence_id} | Organism: {organism} | Protein Name: {protein_name}\n{sequence}"

    if family not in fasta_files:
        fasta_files[family] = []

    fasta_files[family].append(fasta_content)

# Write the FASTA content to files for each Protein Family
for family, fasta_content_list in fasta_files.items():
    family_directory = os.path.join(output_directory, family)
    os.makedirs(family_directory, exist_ok=True)

    fasta_file_path = os.path.join(family_directory, f"{family}.fasta")
    with open(fasta_file_path, "w") as fasta_file:
        fasta_file.write("\n".join(fasta_content_list))

print("One FASTA file created for each Protein Family.")
