from flask import Flask, render_template, request
import os
from collections import Counter
import json

app = Flask(__name__)

# Define color codes for amino acids
amino_acid_colors = {
    'A': '#ff0000', 'R': '#00ff00', 'N': '#0000ff', 'D': '#ff00ff',
    'C': '#ffff00', 'Q': '#00ffff', 'E': '#ff6600', 'G': '#ff3366',
    'H': '#3366ff', 'I': '#66ff33', 'L': '#33ff66', 'K': '#6600ff',
    'M': '#ff33ff', 'F': '#ffff33', 'P': '#33ffff', 'S': '#ccff00',
    'T': '#00ccff', 'W': '#ffcc00', 'Y': '#cc00ff', 'V': '#00ffcc',
    '-': '#cccccc'  # Gap character
}


def get_sequence_details_from_json(json_file_path):
    # Load JSON data from the file
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    
    # Initialize an empty dictionary to store sequence details
    sequence_details = {}
    
    # Iterate through each entry in the JSON data
    for entry in data:
        sequence_id = entry.get("Sequence ID")
        # Store the entry details in the sequence_details dictionary using the sequence ID as the key
        sequence_details[sequence_id] = {
            "Organism": entry.get("Organism", ""),
            "Protein Name": entry.get("Protein Name", ""),
            "Engineered": entry.get("Engineered", ""),
            "Sequence Length": entry.get("Sequence Length", "")
        }
    
    return sequence_details


def parse_fasta(file_path):
    sequences = []
    with open(file_path, 'r') as file:
        sequence_id = None
        sequence = ''
        for line in file:
            if line.startswith('>'):
                if sequence:
                    sequences.append((sequence_id, sequence.replace(' ', '')))  # Append tuple of (sequence_id, sequence)
                    sequence = ''  # Reset sequence for the next sequence
                sequence_id = line.strip()[1:]
            else:
                sequence += line.strip()
        sequences.append((sequence_id, sequence.replace(' ', '')))  # Add the last sequence
    return sequences

def calculate_coverage_consensus(sequences):
    total_length = len(sequences[0])  # Assuming all sequences have the same length
    covered_positions = sum(1 for pos in zip(*sequences) if '-' not in pos)
    coverage_percentage = (covered_positions / total_length) * 100
    
    # Calculate consensus percentage (percentage of positions with the most frequent amino acid)
    consensus_positions = sum(1 for pos in zip(*sequences) if Counter(pos).most_common(1)[0][1] / len(sequences) >= 0.5)
    consensus_percentage = (consensus_positions / total_length) * 100
    
    return coverage_percentage, consensus_percentage



@app.route('/')
def index():
    files = [f for f in os.listdir('NEW_MSA/fasta_files/MSA_align_files') if f.endswith('.fasta')]
    return render_template('load.html', files=files)


@app.route('/visualize', methods=['POST'])
@app.route('/visualize', methods=['POST'])
def visualize():
    selected_file = request.form['file']
    fasta_path = os.path.join('fasta_files/MSA_align_files', selected_file)
    sequences = parse_fasta(fasta_path)
    sequences_with_colors = []
    sequence_details = get_sequence_details_from_json("ProteinDatabase.json")  # Fetch sequence details from JSON file
    
    for sequence_id, sequence in sequences:
        colored_sequence = [(aa, amino_acid_colors.get(aa, '#000000')) for aa in sequence]
        sequences_with_colors.append((sequence_id, colored_sequence))  # Append tuple of (sequence_id, colored_sequence)
        
    coverage_percentage, consensus_percentage = calculate_coverage_consensus([seq for _, seq in sequences])  # Extract sequences from (sequence_id, sequence) tuples
    
    return render_template('test.html', sequences=sequences_with_colors, coverage_percentage=coverage_percentage, consensus_percentage=consensus_percentage, sequence_details=sequence_details)


if __name__ == '__main__':
    app.run(debug=True)
