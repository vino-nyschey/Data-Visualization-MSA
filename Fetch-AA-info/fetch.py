from Bio import SeqIO
from Bio.PDB import PDBList, PDBParser
import re

def extract_pdb_id(sequence_id):
    # Extract PDB ID from the sequence ID
    match = re.search(r'^(\w+):\w$', sequence_id)
    if match:
        return match.group(1)
    else:
        return None

def fetch_protein_info(pdb_id, amino_acid_sequence):
    try:
        # Fetch PDB file
        pdb_list = PDBList()
        pdb_file_path = pdb_list.retrieve_pdb_file(pdb_id, file_format="pdb")

        # Parse PDB file
        parser = PDBParser(QUIET=True)
        structure = parser.get_structure(pdb_id, pdb_file_path)

        # Extract protein name and organism from the PDB header
        header = structure.header
        protein_name = header.get('name', 'N/A')
        organism = header.get('organism_scientific', 'N/A')

        return protein_name, organism

    except Exception as e:
        print(f"Error processing PDB ID {pdb_id}: {str(e)}")
        return 'N/A', 'N/A'

if __name__ == "__main__":
    fasta_file = "input1.fasta"

    # Iterate through sequences in the FASTA file
    for record in SeqIO.parse(fasta_file, "fasta"):
        sequence_id = record.id
        amino_acid_sequence = str(record.seq)

        # Extract PDB ID from the sequence ID
        pdb_id = extract_pdb_id(sequence_id)

        if pdb_id:
            protein_name, organism = fetch_protein_info(pdb_id, amino_acid_sequence)

            print(f"Sequence ID: {sequence_id}")
            print(f"PDB ID: {pdb_id}")
            print(f"Protein Name: {protein_name}")
            print(f"Organism: {organism}")
            print("-" * 40)
        else:
            print(f"Invalid sequence ID format: {sequence_id}")
