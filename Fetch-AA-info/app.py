from flask import Flask, render_template
from datetime import datetime
import pandas as pd
import plotly.offline as pyo
import plotly.express as px
import os

app = Flask(__name__)

def plot_data(data):
    # Convert 'Founded Date' to datetime and extract the year
    data['Founded Year'] = pd.to_datetime(data['Founded Date'], errors='coerce').dt.year

    # Create a scatter plot with PDB ID on the y-axis
    fig = px.scatter(data, x='Founded Year', y='PDB ID', 
                     labels={'Founded Year': 'Founded Year', 'y': 'PDB ID'},
                     title='Protein Founded Year Timeline',
                     template='plotly', height=1200)

    # Update x-axis ticks
    fig.update_xaxes(dtick=1)

    return fig

@app.route('/')
def index():
    # Read data from CSV file
    csv_file_path = 'output_data.csv'
    if not os.path.exists(csv_file_path):
        return "CSV file not found."

    data = pd.read_csv(csv_file_path)

    # Convert founded dates to integers for sorting
    data['Founded Year'] = data['Founded Date'].apply(lambda x: int(x.split('-')[0]) if pd.notnull(x) else None)

    # Create a plot
    plot = plot_data(data)

    # Save the plot as HTML
    plot_html = pyo.plot(plot, output_type='div', include_plotlyjs=False)

    return render_template('timeline-plot.html', graph_html=plot_html)

if __name__ == '__main__':
    app.run(debug=True)
