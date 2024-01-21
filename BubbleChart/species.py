import os
import json
import pandas as pd
import plotly.express as px
from flask import Flask, render_template, request

app = Flask(__name__)

def plot_bubble_chart(data, selected_species=None):
    # Convert 'Discovered Year' to integer
    data['Discovered Year'] = pd.to_numeric(data['Discovered Year'], errors='coerce')

    # Filter data based on selected species
    if selected_species:
        data = data[data['Species Name'].isin(selected_species)]

    # Create a bubble chart with Sequence ID on the x-axis
    fig = px.scatter(data, x='Sequence ID', y='Discovered Year', hover_name='Protein Name',
                     color='Protein Family',  # Differentiate by Protein Family
                     size='No. of Chains',
                     opacity=0.7,  # Set default opacity
                     labels={'x': 'Sequence ID', 'y': 'Discovered Year'},
                     title='Protein Discovered Year Bubble Chart',
                     template='plotly', height=500)

    # Update x-axis ticks
    fig.update_xaxes(dtick=1)

    # Add legends
    fig.update_layout(showlegend=True)

    return fig

def plot_bar_chart(data, selected_species=None):
    # Filter data based on selected species
    if selected_species:
        data = data[data['Species Name'].isin(selected_species)]

    # Create a bar chart with the count of occurrences for each Protein Family
    bar_fig = px.bar(data, y='Protein Family', title='Occurrence Count for Selected Protein Families',
                     color='Species Name',
                     labels={'Protein Family': 'Selected Protein Families', 'count': 'Number of Occurrences'},
                     template='plotly', height=400)

    # Add legends
    bar_fig.update_layout(showlegend=True)

    return bar_fig

@app.route('/', methods=['GET', 'POST'])
def index():
    # Read JSON data from file
    json_file_path = 'ProteinDatabase.json'
    
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
        bar_chart = plot_bar_chart(df, selected_species)
        data = df[df['Species Name'].isin(selected_species)].to_dict(orient='records')
    else:
        # Initial load without species selection
        bubble_chart = plot_bubble_chart(df)
        bar_chart = plot_bar_chart(df)
        data = df.to_dict(orient='records')

    # Save the charts as HTML
    bubble_chart_html = bubble_chart.to_html(full_html=False, include_plotlyjs='cdn')
    bar_chart_html = bar_chart.to_html(full_html=False, include_plotlyjs='cdn')

    return render_template('species_plot.html', species=unique_species,
                           bubble_chart_html=bubble_chart_html, bar_chart_html=bar_chart_html,
                           data=data, selected_species=selected_species)

if __name__ == '__main__':
    app.run(debug=True)
