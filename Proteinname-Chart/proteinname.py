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
    organisms = data_filtered['Organism']
    general_name = [] #grouped names of proteins
    human_proteins = []
    coli_proteins = []
    rest_proteins = []
    labels_chart = [] #general bar plot
    labels_chart_human = [] #only human proteins
    labels_chart_coli = [] #only E.coli proteins
    count_chart = [] #general bar plot
    count_chart_human = [] #only human proteins
    count_chart_coli = [] #only E.coli proteins

    # summarize proteins according to general enzyme groupings
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
    
    #divide proteins according to organism
    for proteinname, organism in zip(general_name, organisms):
       if 'HOMO SAPIENS' == organism:
            human_proteins.append(proteinname)
       elif 'ESCHERICHIA COLI' == organism: 
           coli_proteins.append(proteinname)
       else: 
           rest_proteins.append(proteinname)
    
    all_proteins = list(set(general_name))
    count_human_proteins = dict(sorted(dict(Counter({label: 0 for label in all_proteins})).items())) #each dictionary contains same protein names
    count_coli_proteins = dict(sorted(dict(Counter({label: 0 for label in all_proteins})).items()))
    count_rest_proteins = dict(sorted(dict(Counter({label: 0 for label in all_proteins})).items()))
    human = dict(Counter(human_proteins))
    count_human_proteins.update(human)
    coli = dict(Counter(coli_proteins))
    count_coli_proteins.update(coli)
    rest = dict(Counter(rest_proteins))
    count_rest_proteins.update(rest)


    #human proteins
    for proteinname, number in count_human_proteins.items():
        if proteinname.upper() != 'NAN': 
            labels_chart_human.append(proteinname)
            count_chart_human.append(number)
    
    #E.coli proteins
    for proteinname, number in count_coli_proteins.items():
        if proteinname.upper() != 'NAN': 
            labels_chart_coli.append(proteinname)
            count_chart_coli.append(number)
    
    #rest proteins
    for proteinname, number in count_rest_proteins.items():
        if proteinname.upper() != 'NAN': 
            labels_chart.append(proteinname)
            count_chart.append(number)

    #create bar chart
    fig = go.Figure()

    #add traces
    fig.add_trace(go.Bar(
            x=count_chart,
            y=labels_chart,
            orientation='h',
            name='other proteins',
            marker_color = 'blue'))
    
    fig.add_trace(go.Bar(
            x=count_chart_human,
            y=labels_chart_human,
            orientation='h',
            name='Homo Sapiens proteins',
            marker_color = "red"))
    
    fig.add_trace(go.Bar(
            x=count_chart_coli,
            y=labels_chart_coli,
            orientation='h',
            name='E.coli proteins',
            marker_color = 'orange'))
    
    fig.update_layout(
    updatemenus=[
        dict(
            x=0, 
            y=1.2,
            active=0,
            buttons=list([
                dict(label="all Organisms",
                     method="update",
                     args=[{"visible": [True, True, True]}]),
                dict(label="other proteins",
                     method="update",
                     args=[{"visible": [True, False, False]}]),
                dict(label="Homo Sapiens proteins",
                     method="update",
                     args=[{"visible": [False, True, False]}]),
                dict(label="E.coli proteins",
                     method="update",
                     args=[{"visible": [False, False, True]}]),
            ]),
        )
    ])

    fig.update_layout(barmode='stack')
    fig.update_layout(hovermode="x unified") #hovermode
    chart_data = json.loads(fig.to_json()) #save as json

    #return the dictionary
    return chart_data

@app.route('/')
def main():
    return render_template('index_proteinname.html', bar_chart=create_chart())

if __name__ == '__main__':
    app.run(debug=True)