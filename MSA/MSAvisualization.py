import os
import dash_bio as dashbio
from dash import Dash, html, Input, Output, dcc
import urllib.parse

app = Dash(__name__)

fasta_folder = 'MSA//MSA_align_files'
fasta_files = [file for file in os.listdir(fasta_folder) if file.endswith('.fasta')]

# dropdown menu
dropdown_options = [{'label': file, 'value': file} for file in fasta_files]

# Load data
def load_data(filename):
    file_path = os.path.join(fasta_folder, filename)
    with open(file_path, 'r') as file:
        data = file.read()
    return data

# layout
app.layout = html.Div([
    dcc.Dropdown(
        id='fasta-dropdown',
        options=dropdown_options,
        value=fasta_files[0] if fasta_files else None
    ),
    dashbio.AlignmentChart(
        id='alignment-viewer',
        data=load_data(fasta_files[0]) if fasta_files else '',
        height=900,
        tilewidth=30
    )
])

# callback to update alignment viewer
@app.callback(
    Output('alignment-viewer', 'data'),
    [Input('fasta-dropdown', 'value')]
)
def update_alignment_viewer(selected_file):
    if selected_file:
        return load_data(selected_file)
    else:
        return ''

if __name__ == '__main__':
    app.run_server(debug=True)
