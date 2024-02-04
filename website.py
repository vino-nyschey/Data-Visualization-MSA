from flask import Flask, render_template, redirect, url_for, request, jsonify
import os
import json
import pandas as pd

from BubbleChart.species import plot_bubble_chart, plot_pie_chart
from Organism_Chart.organism import create_pie_chart
from Proteinname_Chart.proteinname import create_bar_chart
from MSA_FLASK.modifiedMSA import get_sequence_details_from_json, parse_fasta, calculate_coverage_consensus, color_patterns
  
app = Flask(__name__, static_url_path='/static')


# Load protein data
json_file_path = "./Database/ProteinDatabase.json"

if os.path.exists(json_file_path):
    with open(os.path.abspath(json_file_path), 'r') as json_file:
        protein_data = json.load(json_file)
        
else:
    protein_data = []
    

@app.route('/')
def index():
    return render_template('base.html', data=protein_data)  # Pass protein_data to template

@app.route('/get_protein_details', methods=['POST'])
def get_protein_details():
    sequence_id = request.json['sequence_id']
    selected_protein = next((protein for protein in protein_data if protein['Sequence ID'] == sequence_id), None)
    if selected_protein:
        return jsonify(selected_protein)
    else:
        return jsonify({})


@app.route('/visualisations', methods=['GET', 'POST'])
def chart():
    # Read JSON data from file
    json_file_path = 'Database/ProteinDatabase.json'
    
    if not os.path.exists(json_file_path):
        return "Error: JSON file not found. Please make sure the file exists."

    # Load JSON data into a DataFrame
    with open(json_file_path, 'r') as json_file:
        json_data = json.load(json_file)

    # Convert the JSON data to a DataFrame
    df = pd.json_normalize(json_data)

    # Get unique species names for checkbox buttons
    unique_species = sorted(df['Species Name'].unique())

    # Initialize selected_species outside of the if-else block
    selected_species = {}

    # Inside the Flask route
    if request.method == 'POST' and 'update_plots' in request.form:
        selected_species = request.form.getlist('species') if request.form.getlist('species') else unique_species
        bubble_chart = plot_bubble_chart(df, selected_species)
        pie_chart = plot_pie_chart(df, selected_species)
        proteinname_plot = create_bar_chart(selected_species)
        organism_plot = create_pie_chart(selected_species)
        data = df[df['Species Name'].isin(selected_species)].to_dict(orient='records')
    else:
        selected_species = unique_species
        bubble_chart = plot_bubble_chart(df, selected_species)
        pie_chart = plot_pie_chart(df, selected_species)
        data = df.to_dict(orient='records')
        proteinname_plot = create_bar_chart(selected_species)
        organism_plot = create_pie_chart(selected_species)
    
    # Save the charts as HTML
    bubble_chart_html = bubble_chart.to_html(full_html=False, include_plotlyjs='cdn')
    pie_chart_html = pie_chart.to_html(full_html=False, include_plotlyjs='cdn')

    return render_template('index.html', species=unique_species,
                           bubble_chart_html=bubble_chart_html, pie_chart_html=pie_chart_html,
                           data=data, selected_species=selected_species, chart_data_org=organism_plot, chart_data_pro=proteinname_plot)

@app.route('/select')
def load():
    files = [f for f in os.listdir('./MSA_FLASK/fasta_files/MSA_align_files') if f.endswith('.fasta')]
    return render_template('load.html', files=files)

@app.route('/msa', methods=['GET', 'POST'])
def visualize():
    selected_file = request.form.get('file')
    if not selected_file:
        return "No file selected.", 400
    
    fasta_path = os.path.join('./MSA_FLASK/fasta_files/MSA_align_files', selected_file)
    if not os.path.exists(fasta_path):
        return "Selected file not found.", 404
    
    sequences = parse_fasta(fasta_path)
    if not sequences:
        return "No sequences found in the file.", 404
    
    sequence_details = get_sequence_details_from_json("./Database/ProteinDatabase.json")
    if not sequence_details:
        return "Error loading sequence details.", 500
    
    coverage_percentages, consensus_percentages = calculate_coverage_consensus(sequences)

    return render_template('visualize.html', sequences=sequences, sequence_details=sequence_details,
                           coverage_percentages=coverage_percentages, consensus_percentages=consensus_percentages,
                           color_patterns=color_patterns)
if __name__ == '__main__':
    app.run(debug=True)