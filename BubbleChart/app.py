import os
import json
import pandas as pd
import plotly.express as px
import plotly.offline as pyo
from flask import Flask, render_template

app = Flask(__name__)

def plot_data(data):
    # Convert 'Discovered Year' to integer
    data['Discovered Year'] = pd.to_numeric(data['Discovered Year'], errors='coerce')

    # Create a bubble chart with PDB ID on the x-axis
    fig = px.scatter(data, x='PDB ID', y='Discovered Year',
                     size='No. of Chains',
                     color='Protein Family',
                     opacity=0.6,  # Set default opacity
                     labels={'x': 'PDB ID', 'y': 'Discovered Year'},
                     title='Protein Discovered Year Bubble Chart',
                     template='plotly', height=600)

    # Update x-axis ticks
    fig.update_xaxes(dtick=1)

    # The 'text' argument specifies what information to display when hovering over a point
    fig.update_traces(text=data['Protein Name'], hoverinfo='text', hovertemplate='%{text}')

    # Add legends
    fig.update_layout(showlegend=True)

    return fig

@app.route('/')
def index():
    # Read JSON data from file
    json_file_path = 'ProteinDatabase.json'
    
    if not os.path.exists(json_file_path):
        return "Error: JSON file not found. Please make sure the file exists."

    # Load JSON data into a DataFrame
    with open(json_file_path, 'r') as json_file:
        json_data = pd.json_normalize(json.load(json_file))

    # Create a plot
    plot = plot_data(json_data)

    # Save the plot as HTML
    plot_html = pyo.plot(plot, output_type='div', include_plotlyjs=False)

    return render_template('timeline-plot.html', graph_html=plot_html)

if __name__ == '__main__':
    app.run(debug=True)
