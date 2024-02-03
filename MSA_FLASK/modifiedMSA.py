from flask import Flask, render_template, request
import os
from collections import Counter
import json

app = Flask(__name__)


# Define color patterns for amino acid coloring in JavaScript
color_patterns = {
    'Clustal': ['#ff6666', '#66ff66', '#6666ff', '#ffff66', '#ff66ff', '#66ffff', '#ff9966', '#ff6666', '#66ff66', '#6666ff', '#ffff66', '#ff66ff', '#66ffff', '#ff9966', '#ff6666', '#66ff66', '#6666ff', '#ffff66', '#ff66ff', '#66ffff', '#ff9966'],
    'Lesk': ['#ff9999', '#ccffcc', '#99ccff', '#ffff99', '#ff99ff', '#99ffff', '#ffcc99', '#ff9999', '#ccffcc', '#99ccff', '#ffff99', '#ff99ff', '#99ffff', '#ffcc99', '#ff9999', '#ccffcc', '#99ccff', '#ffff99', '#ff99ff', '#99ffff', '#ffcc99'],
    'Custom': ['#ff0000', '#00ff00', '#0000ff', '#ffff00', '#ff00ff', '#00ffff', '#ff6600', '#ff3366', '#3366ff', '#66ff33', '#33ff66', '#6600ff', '#ff33ff', '#ffff33', '#33ffff', '#ccff00', '#00ccff', '#ffcc00', '#cc00ff', '#00ffcc', '#cccccc']
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
            "Sequence Length": entry.get("Sequence Length", ""),
            "No. of Chains": entry.get("No. of Chains", "")
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
    total_length = len(sequences[0][1])  # Assuming all sequences have the same length
    coverage_percentages = []
    consensus_percentages = []

    for i in range(total_length):
        column = [seq[1][i] for seq in sequences if seq[1][i] != '-']  # Exclude "-" characters
        if column:  # Check if column is not empty
            coverage_percentage = (column.count('-') / len(column)) * 100
            consensus_percentage = (Counter(column).most_common(1)[0][1] / len(column)) * 100
        else:
            coverage_percentage = 100  # All sequences are gaps in this column
            consensus_percentage = 0
        coverage_percentages.append(coverage_percentage)
        consensus_percentages.append(consensus_percentage)

    return coverage_percentages, consensus_percentages

@app.route('/')
def index():
    files = [f for f in os.listdir('fasta_files/MSA_align_files') if f.endswith('.fasta')]
    return render_template('load.html', files=files)

@app.route('/visualize', methods=['POST'])
def visualize():
    selected_file = request.form.get('file')
    if not selected_file:
        return "No file selected.", 400
    
    fasta_path = os.path.join('fasta_files/MSA_align_files', selected_file)
    if not os.path.exists(fasta_path):
        return "Selected file not found.", 404
    
    sequences = parse_fasta(fasta_path)
    if not sequences:
        return "No sequences found in the file.", 404
    
    sequence_details = get_sequence_details_from_json("ProteinDatabase.json")
    if not sequence_details:
        return "Error loading sequence details.", 500
    
    coverage_percentages, consensus_percentages = calculate_coverage_consensus(sequences)

    return render_template('visualize.html', sequences=sequences, sequence_details=sequence_details,
                           coverage_percentages=coverage_percentages, consensus_percentages=consensus_percentages,
                           color_patterns=color_patterns)

if __name__ == '__main__':
    app.run(debug=True)
