from flask import Flask, render_template
import pandas as pd
from collections import Counter
from pathlib import Path
import plotly.graph_objects as go
import json

app = Flask(__name__)

def create_chart():
    # data for the pie chart
    root_folder = Path(__file__).parents[1]
    my_path = root_folder / "Fetch-AA-info/output_data.csv"

    data =  pd.read_csv(my_path)
    data_filtered = data[data['Sequence ID'].str.split(':').str[1] == 'A'] # to get each protein once independent on how many chains it has
    proteinnames = data_filtered['Protein Name']
    general_name = []

    for proteinname in proteinnames:
        proteinname = str(proteinname)
        if 'LIPASE' in proteinname.upper(): 
            general_name.append('Lipase')
        elif 'PHOSPHATASE' in proteinname.upper(): 
            general_name.append('Phosphatase')
        elif 'TRANSFERASE' in proteinname.upper(): 
            general_name.append('Transferase')
        elif 'KINASE' in proteinname.upper(): 
            general_name.append('Kinase')
        elif 'ESTERASE' in proteinname.upper(): 
            general_name.append('Esterase')
        elif 'HYDROLASE' in proteinname.upper(): 
            general_name.append('Hydrolase')
        else: 
            general_name.append(proteinname)
    
    labels_chart = []
    count_chart = []
    count_proteinnames = Counter(general_name)
    for proteinname, number in count_proteinnames.items():
        if proteinname.upper() != 'NAN': 
            labels_chart.append(f"{proteinname}")
            count_chart.append(number)

    # create bar chart
    fig = go.Figure(go.Bar(
            x=count_chart,
            y=labels_chart,
            orientation='h',
            hovertemplate=None))

    fig.update_layout(hovermode="x")
    chart_data = json.loads(fig.to_json())

    # Return the dictionary
    return chart_data

@app.route('/')
def main():
    return render_template('index_proteinname.html', bar_chart=create_chart())

if __name__ == '__main__':
    app.run(debug=True)