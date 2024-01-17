from Bio import SeqIO
from Bio.PDB import PDBList
import os
import re

def download_pdb_file(pdb_id, output_folder="PDB-Database"):
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Set the output path for the PDB file
    pdb_file_path = os.path.join(output_folder, f"{pdb_id.lower()}.pdb")

    # Download PDB file using PDBList
    pdbl = PDBList()
    pdbl.retrieve_pdb_file(pdb_id, file_format="pdb", pdir=output_folder)

    return pdb_file_path

fasta_file = "input1.fasta"

# Iterate through sequences in the FASTA file
for record in SeqIO.parse(fasta_file, "fasta"):
    sequence_id = record.id

    # Extract PDB ID from the sequence ID
    match = re.search(r'^(\w+):\w$', sequence_id)
    if match:
        pdb_id = match.group(1)

        # Download PDB file for the current sequence into the "PDB-Database" folder
        downloaded_pdb_file = download_pdb_file(pdb_id)
        print(f"PDB file downloaded for Sequence ID {sequence_id}: {downloaded_pdb_file}")
    
    else:
        print(f"Invalid sequence ID format: {sequence_id}")
