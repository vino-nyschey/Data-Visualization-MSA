from flask import Flask, render_template, redirect, url_for, request
import os
import json
import pandas as pd

from BubbleChart.species import plot_bubble_chart, plot_pie_chart
from Organism_Chart.organism import create_pie_chart
from Proteinname_Chart.proteinname import create_bar_chart
  
app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
    return redirect(url_for('base'))

@app.route('/base')
def base():
    return render_template('base.html')

@app.route('/species', methods=['GET', 'POST'])
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
    unique_species = df['Species Name'].unique()

    # Initialize selected_species outside of the if-else block
    selected_species = None

    # Inside the Flask route
    if request.method == 'POST':
        selected_species = request.form.getlist('species')
        bubble_chart = plot_bubble_chart(df, selected_species)
        pie_chart = plot_pie_chart(df, selected_species)
        data = df[df['Species Name'].isin(selected_species)].to_dict(orient='records')
    else:
        # Initial load without species selection
        bubble_chart = plot_bubble_chart(df)
        pie_chart = plot_pie_chart(df)
        data = df.to_dict(orient='records')

    # Save the charts as HTML
    bubble_chart_html = bubble_chart.to_html(full_html=False, include_plotlyjs='cdn')
    pie_chart_html = pie_chart.to_html(full_html=False, include_plotlyjs='cdn')

    #plot other charts
    organism_plot = create_pie_chart()
    proteinname_plot = create_bar_chart()

    return render_template('species_plot.html', species=unique_species,
                           bubble_chart_html=bubble_chart_html, pie_chart_html=pie_chart_html,
                           data=data, selected_species=selected_species, chart_data_org=organism_plot, chart_data_pro=proteinname_plot)

if __name__ == '__main__':
    app.run(debug=True)