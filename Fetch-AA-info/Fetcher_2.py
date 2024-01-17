import os
import re
import json
import csv
import collections

from Bio import SeqIO


def extract_pdb_id_and_chain(sequence_id):
    # Extract PDB ID and chain from the sequence ID
    match = re.match(r'^(\w+):(\w)$', sequence_id)
    if match:
        return match.group(1), match.group(2)
    else:
        return None, None

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

import re

def extract_protein_info_from_compnd(pdb_file_path):
    # Extract protein names and engineered information from the COMPND section
    protein_name_mapping = {}
    engineered_values = {}

    with open(pdb_file_path, 'r') as pdb_file:
        in_molecule_section = False
        current_protein_name = None
        current_engineered = 'NO'
        current_chains = []

        for line in pdb_file:
            if line.startswith("COMPND"):
                molecule_match = re.search(r'MOLECULE: (.+);', line)
                engineered_match = re.search(r'ENGINEERED: (\w+);', line)
                chain_match = re.search(r'CHAIN: ([A-Z, ]+);', line)

                if molecule_match:
                    current_protein_name = molecule_match.group(1).strip()
                    # Exclude "PROTEIN (" prefix and ")" suffix
                    if current_protein_name.startswith("PROTEIN (") and current_protein_name.endswith(")"):
                        current_protein_name = current_protein_name[len("PROTEIN ("):-1].strip()

                elif engineered_match:
                    current_engineered = engineered_match.group(1).strip()

                elif chain_match:
                    current_chains = [chain.strip() for chain in chain_match.group(1).split(',')]

                    # Associate each chain with the current protein name
                    for chain in current_chains:
                        protein_name_mapping[chain] = current_protein_name
                        engineered_values[chain] = current_engineered

    return protein_name_mapping, engineered_values


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
            # Extract protein name and engineered information from the COMPND section
            protein_name, engineered = extract_protein_info_from_compnd(pdb_file_path)

            # Extract founded date from the HEADER line
            founded_date = extract_founded_date_from_header(pdb_file_path)

            # Extract organism information from the PDB file
            organism = extract_organism(pdb_file_path)

            return protein_name, founded_date, organism, engineered
        else:
            raise FileNotFoundError(f"PDB file not found for ID {pdb_id}")

    except FileNotFoundError as e:
        print(f"Error: {str(e)}")
        return 'N/A', 'N/A', 'N/A', 'N/A'
    except Exception as e:
        print(f"Error processing PDB ID {pdb_id}: {str(e)}")
        return 'N/A', 'N/A', 'N/A', 'N/A'

def export_to_json(data, json_filename):
    # Export data to a JSON file
    with open(json_filename, 'w', newline='') as json_file:
        json.dump(data, json_file, indent=2)

def main():
    input_fasta_file = "input1.fasta"
    output_json_file = "fetched_data.json"

    data_to_export = []

    # Iterate through sequences in the FASTA file
    for record in SeqIO.parse(input_fasta_file, "fasta"):
        sequence_id = record.id
        amino_acid_sequence = str(record.seq)

        # Extract PDB ID and chain from the sequence ID
        pdb_id, chain = extract_pdb_id_and_chain(sequence_id)

        if pdb_id and chain:
            protein_names, founded_date, organism, engineered = fetch_protein_info(pdb_id, amino_acid_sequence)

            # Include only the relevant information for the current chain
            relevant_protein_name = protein_names.get(chain, 'N/A')
            relevant_engineered = engineered.get(chain, 'NO')

            # Append the data to the list
            data_to_export.append({
                'Sequence ID': f"{pdb_id}:{chain}",
                'PDB ID': pdb_id,
                'Protein Name': relevant_protein_name,
                'Founded Date': founded_date,
                'Organism': organism,
                'Engineered': relevant_engineered,
                'Sequence': amino_acid_sequence,
                'Sequence Length': len(amino_acid_sequence)
            })

            print(f"Sequence ID: {pdb_id}:{chain}")
            print(f"PDB ID: {pdb_id}")
            print(f"Protein Name: {relevant_protein_name}")
            print(f"Founded Date: {founded_date}")
            print(f"Organism: {organism}")
            print(f"Engineered: {relevant_engineered}")
            print(f"Sequence: {amino_acid_sequence}")
            print(f"Sequence Length: {len(amino_acid_sequence)}")
            print("-" * 40)
        else:
            print(f"Invalid sequence ID format: {sequence_id}")

    # Export the data to JSON
    export_to_json(data_to_export, output_json_file)
    print(f"Data exported to {output_json_file}")


if __name__ == "__main__":
    main()