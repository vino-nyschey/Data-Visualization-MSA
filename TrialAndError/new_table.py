import dash
from dash import html, callback, Output, Input
from dash.dash_table import DataTable
import json

# Load protein data from the JSON file
with open('ProteinDatabase.json', 'r') as file:
    protein_data = json.load(file)

app = dash.Dash(__name__)

# Define the layout with three parts: upper half for table, lower half divided into left and right sides with a vertical line
app.layout = html.Div([
    html.Div([
        DataTable(
            id='table',
            columns=[{'name': col, 'id': col} for col in protein_data[0].keys() if col not in ['Sequence', 'Species Name']],
            data=[{col: row[col] for col in protein_data[0].keys() if col not in ['Sequence', 'Species Name']} for row in protein_data],
            selected_rows=[],
            row_deletable=False,  # Set row_deletable to False to hide the "select" button
            style_table={'maxHeight': 'calc(50vh - 20px)', 'overflowY': 'scroll'},  # Upper half for table
        ),
        html.Hr(),  # Horizontal line below the table
    ], style={'marginBottom': 20}),
    
    html.Div([
        html.Div([
            html.Div(id='pdb-file-name', style={'textAlign': 'center'}),  # Left side for PDB file name
            html.H2("Protein Overview:", style={'textAlign': 'center'}),  # Heading for Protein Overview
            html.Hr(),  # Horizontal line above the Protein Overview section
        ], style={'flex': '1', 'borderRight': '1px solid #ccc', 'paddingRight': '20px'}),
        
        html.Div([
            html.Div(id='protein-details', style={'whiteSpace': 'pre', 'fontFamily': 'monospace', 'fontSize': 12}),  # Right side for protein details
            html.Div(id='sequence-details', style={'whiteSpace': 'pre', 'fontFamily': 'monospace', 'fontSize': 12}),  # Right side for sequence details
        ], style={'flex': '1', 'paddingLeft': '20px'}),
    ], style={'display': 'flex'}),
])

# Function to generate unique color for each letter
def get_letter_color(letter):
    color_code = hash(letter) % (16**6)
    return f"#{color_code:06x}"

# Callback to update protein details and sequence details
@app.callback(
    Output('pdb-file-name', 'children'),
    Output('protein-details', 'children'),
    Output('sequence-details', 'children'),
    [Input('table', 'active_cell')]
)
def update_protein_details(selected_cell):
    if selected_cell and selected_cell['column_id'] == 'Sequence ID':
        sequence_id = protein_data[selected_cell['row']]['Sequence ID']
        selected_protein = [protein for protein in protein_data if protein['Sequence ID'] == sequence_id][0]

        pdb_file_name = html.Div([
            html.Strong("PDB File Name:"),
            html.Br(),
            f"pdb{selected_protein['PDB ID'].lower()}.ent",  # Formatted PDB file name
        ])

        protein_details = html.Div([
            html.Div(f"PDB ID: {selected_protein['PDB ID']}"),
            html.Div(f"Organism: {selected_protein['Organism']}"),
            html.Div(f"Engineered: {selected_protein['Engineered']}"),
            html.Div(f"No. of Chains: {selected_protein['No. of Chains']}"),
            html.Div(f"Sequence ID: {selected_protein['Sequence ID']}"),
            html.Div(f"Protein Name: {selected_protein['Protein Name']}"),
            html.Div(f"Protein Family: {selected_protein['Protein Family']}"),
            html.Div(f"Sequence Length: {selected_protein['Sequence Length']}"),
        ])

        sequence = selected_protein.get('Sequence', 'N/A')
        formatted_sequence = [
            html.Span(letter, style={'color': get_letter_color(letter), 'fontFamily': 'monospace'})
            if (i + 1) % 60 != 0 or i == 0 else html.Br()
            for i, letter in enumerate(sequence)
        ]

        sequence_details = html.Div([
            html.Strong(f"Sequence ID: {selected_protein['Sequence ID']}"),
            html.Br(),
            html.Div(formatted_sequence),
        ])

        return pdb_file_name, protein_details, sequence_details

    return "", "", ""

if __name__ == '__main__':
    app.run_server(debug=True)
