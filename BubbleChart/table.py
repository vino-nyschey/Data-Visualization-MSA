import os
import json
import pandas as pd
from flask import Flask, render_template

app = Flask(__name__)

def load_protein_data():
    # Read JSON data from file
    
    json_file_path = "Database/ProteinDatabase.json"

    if not os.path.exists(json_file_path):
        return None

    # Load JSON data into a DataFrame
    with open(json_file_path, 'r') as json_file:
        json_data = json.load(json_file)

    # Convert the JSON data to a DataFrame
    df = pd.json_normalize(json_data)

    return df

@app.route('/')
def index():
    # Load protein data
    protein_data = load_protein_data()

    if protein_data is None:
        return "Error: JSON file not found. Please make sure the file exists."

    # Pass the protein data to the template
    return render_template('table.html', data=protein_data.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
