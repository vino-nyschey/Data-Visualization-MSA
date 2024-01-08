from Bio import SeqIO
from Bio.PDB import PDBParser
import os
import re
import csv

def extract_pdb_id(sequence_id):
    # Extract PDB ID from the sequence ID
    match = re.search(r'^(\w+):\w$', sequence_id)
    if match:
        return match.group(1)
    else:
        return None

def extract_organism(pdb_file_path):
    # Extract organism information from the SOURCE record in the PDB file
    organism = 'N/A'
    with open(pdb_file_path, 'r') as pdb_file:
        for line in pdb_file:
            if line.startswith("SOURCE"):
                match = re.search(r'ORGANISM_SCIENTIFIC: (.+);', line)
                if match:
                    organism = match.group(1)
                    break
    return organism

def extract_protein_info_from_compnd(pdb_file_path):
    # Extract protein name from the "MOLECULE:" line in the COMPND section
    protein_name = 'N/A'
    with open(pdb_file_path, 'r') as pdb_file:
        in_molecule_section = False
        for line in pdb_file:
            if line.startswith("COMPND"):
                match = re.search(r'MOLECULE: (.+);', line)
                if match:
                    protein_name = match.group(1)
                    break
            
    return protein_name

def extract_founded_date_from_header(pdb_file_path):
    # Extract founded date from the HEADER line
    founded_date = 'N/A'
    with open(pdb_file_path, 'r') as pdb_file:
        for line in pdb_file:
            if line.startswith("HEADER"):
                # Capture the entire line after "HEADER"
                header_content = line.split("HEADER", 1)[1].strip()
                
                # Attempt to extract the date from the captured content
                match = re.search(r'(\d+-\w+(?:-\d{2,4})?)', header_content)
                
                if match:
                    founded_date = match.group(1)
                    break

    return founded_date





def find_pdb_file(pdb_id):
    # Search for PDB files recursively within the current working directory
    for root, dirs, files in os.walk(os.getcwd()):
        for file in files:
            if file.lower() == f"pdb{pdb_id.lower()}.ent":
                return os.path.join(root, file)
    return None

def fetch_protein_info(pdb_id, amino_acid_sequence):
    try:
        # Find the full path to the PDB file
        pdb_file_path = find_pdb_file(pdb_id)

        if pdb_file_path:
            # Extract protein name from the COMPND section
            protein_name = extract_protein_info_from_compnd(pdb_file_path)

            # Extract founded date from the HEADER line
            founded_date = extract_founded_date_from_header(pdb_file_path)

            # Extract organism information from the PDB file
            organism = extract_organism(pdb_file_path)

            return protein_name, founded_date, organism
        else:
            raise FileNotFoundError(f"PDB file not found for ID {pdb_id}")

    except Exception as e:
        print(f"Error processing PDB ID {pdb_id}: {str(e)}")
        return 'N/A', 'N/A', 'N/A'
    
def export_to_csv(data, csv_filename):
    # Export data to a CSV file
    with open(csv_filename, 'w', newline='') as csv_file:
        fieldnames = ['Sequence ID', 'PDB ID', 'Protein Name', 'Founded Date', 'Organism']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # Write the header
        writer.writeheader()

        # Write the data rows
        for row in data:
            writer.writerow(row)

if __name__ == "__main__":
    fasta_file = "input1.fasta"
    output_csv_file = "output_data.csv"
    data_to_export = []

    # Iterate through sequences in the FASTA file
    for record in SeqIO.parse(fasta_file, "fasta"):
        sequence_id = record.id
        amino_acid_sequence = str(record.seq)

        # Extract PDB ID from the sequence ID
        pdb_id = extract_pdb_id(sequence_id)

        if pdb_id:
            protein_name, founded_date, organism = fetch_protein_info(pdb_id, amino_acid_sequence)

            # Append the data to the list
            data_to_export.append({
                'Sequence ID': sequence_id,
                'PDB ID': pdb_id,
                'Protein Name': protein_name,
                'Founded Date': founded_date,
                'Organism': organism
            })

            print(f"Sequence ID: {sequence_id}")
            print(f"PDB ID: {pdb_id}")
            print(f"Protein Name: {protein_name}")
            print(f"Founded Date: {founded_date}")
            print(f"Organism: {organism}")
            print("-" * 40)
        else:
            print(f"Invalid sequence ID format: {sequence_id}")

    # Export the data to CSV
    export_to_csv(data_to_export, output_csv_file)
    print(f"Data exported to {output_csv_file}")