from flask import Flask, render_template, redirect, url_for, request, jsonify
import os
import json
import pandas as pd

from BubbleChart.species import plot_bubble_chart, plot_pie_chart
from Organism_Chart.organism import create_pie_chart
from Proteinname_Chart.proteinname import create_bar_chart
  
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

if __name__ == '__main__':
    app.run(debug=True)