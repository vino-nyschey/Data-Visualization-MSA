from flask import Flask, render_template
import csv
import plotly.express as px
from datetime import datetime

app = Flask(__name__)

def read_csv(file_path):
    # Read data from the CSV file and sort by Founded Date
    data = []
    with open(file_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            # Convert Founded Date to datetime object for sorting
            row['Founded Date'] = datetime.strptime(row['Founded Date'], '%d-%b-%y') if row['Founded Date'] != 'N/A' else None
            data.append(row)

    # Sort data by Founded Date
    sorted_data = sorted(data, key=lambda x: (x['Founded Date'] or datetime.max, x['PDB ID']))
    return sorted_data

def create_scatter_plot(data):
    # Filter data to use only one protein per PDB (you can customize this logic)
    unique_pdbs = set()
    filtered_data = []
    for row in data:
        pdb_id = row['PDB ID']
        if pdb_id not in unique_pdbs:
            unique_pdbs.add(pdb_id)
            filtered_data.append(row)

    # Create scatter plot
    fig = px.scatter(filtered_data, x='Founded Date', y='Protein Name', hover_data=['Sequence ID', 'PDB ID', 'Organism'],
                     title='Protein Name vs Founded Date (One Protein per PDB)')
    return fig

@app.route('/')
def index():
    # Render the index page with protein information and scatter plot
    csv_file = "output_data.csv"
    data = read_csv(csv_file)
    scatter_plot = create_scatter_plot(data)
    scatter_plot_div = scatter_plot.to_html(full_html=False)

    return render_template('index_with_plot.html', data=data, scatter_plot_div=scatter_plot_div)

if __name__ == '__main__':
    app.run(debug=True)
