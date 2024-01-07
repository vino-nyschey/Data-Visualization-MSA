from flask import Flask, render_template, request

from Bio import SeqIO

app = Flask(__name__)

# Function to parse the FASTA file and extract sequence information
def parse_fasta(file_path):
    sequences = []
    with open(file_path, "r") as fasta_file:
        for record in SeqIO.parse(fasta_file, "fasta"):
            # Split the sequence name to extract protein name and chain ID
            parts = record.id.split('|')
            protein_name, chain_id = parts[0], parts[2]

            sequences.append({
                "name": record.id,
                "protein_name": protein_name,
                "chain_id": chain_id,
                "length": len(record.seq),
                "sequence": str(record.seq)
            })
    return sequences

# Route for the home page
@app.route('/')
def index():
    fasta_file_path = "input.fasta"
    sequences = parse_fasta(fasta_file_path)

    # Sorting based on user's choice
    sort_by = request.args.get('sort_by', default=None)
    if sort_by == 'length':
        sequences = sorted(sequences, key=lambda x: x['length'])
    elif sort_by == 'name':
        sequences = sorted(sequences, key=lambda x: x['name'])

    return render_template('index.html', sequences=sequences)

# Route for the sequence view page
@app.route('/view_sequence/<seq_name>')
def view_sequence(seq_name):
    fasta_file_path = "input.fasta"
    sequences = parse_fasta(fasta_file_path)
    selected_sequence = next((seq for seq in sequences if seq["name"] == seq_name), None)
    return render_template('view_sequence.html', sequence=selected_sequence)

if __name__ == '__main__':
    app.run(debug=True)
