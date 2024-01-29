import os
import json
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Load protein data
json_file_path = "Data-Visualization-MSA//Database//ProteinDatabase.json"

if os.path.exists(json_file_path):
    with open(json_file_path, 'r') as json_file:
        protein_data = json.load(json_file)
        print("Loaded protein data:", protein_data)  # Debugging statement
else:
    protein_data = []
    print("JSON file not found")  # Debugging statement

@app.route('/')
def index():
    return render_template('index.html', data=protein_data)  # Pass protein_data to template

@app.route('/get_protein_details', methods=['POST'])
def get_protein_details():
    sequence_id = request.json['sequence_id']
    selected_protein = next((protein for protein in protein_data if protein['Sequence ID'] == sequence_id), None)
    if selected_protein:
        return jsonify(selected_protein)
    else:
        return jsonify({})

if __name__ == '__main__':
    app.run(debug=True)
