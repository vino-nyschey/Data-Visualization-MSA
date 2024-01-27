import pandas as pd
from collections import Counter
from pathlib import Path
import plotly.graph_objects as go
import plotly.io as pio

def categorization(): 
    root_folder = Path(__file__).parents[1]
    my_path = root_folder / "Database/fetched_data.csv"
    data =  pd.read_csv(my_path)
    data_filtered = data[data['Sequence ID'].str.split(':').str[1] == 'A'] # to get each protein once independent on how many chains it has
    proteinnames = data_filtered['Protein Name']
    organisms = data_filtered['Organism']
    general_name = [] #grouped names of proteins
    other_names = [] #protein names part of category other

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
        elif 'PEPTIDE' in proteinname.upper(): 
            general_name.append('Peptide')
        elif 'PHOSPHORYLASE' in proteinname.upper(): 
            general_name.append('Phosphorylase')
        elif 'POLYMERASE' in proteinname.upper(): 
            general_name.append('Polymerase')
        else: 
            general_name.append('Other')
            other_names.append(proteinname) 

    return general_name, other_names, organisms

def divideByOrganism(general_name, organisms): 
    human_proteins = [] #protein names of human proteins
    coli_proteins = [] #protein names of E.coli proteins
    rest_proteins = [] #protein names of other proteins

     #divide proteins according to organism
    for proteinname, organism in zip(general_name, organisms):
       if 'HOMO SAPIENS' == organism:
            human_proteins.append(proteinname)
       elif 'ESCHERICHIA COLI' == organism: 
           coli_proteins.append(proteinname)
       else: 
           rest_proteins.append(proteinname)

    return human_proteins, coli_proteins, rest_proteins

def labelChart(general_name, human_proteins, coli_proteins, rest_proteins): 
    labels_chart = [] #general bar plot
    labels_chart_human = [] #only human proteins
    labels_chart_coli = [] #only E.coli proteins
    count_chart = [] #general bar plot
    count_chart_human = [] #only human proteins
    count_chart_coli = [] #only E.coli proteins
    
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
        labels_chart_human.append(proteinname)
        count_chart_human.append(number)
    
    #E.coli proteins
    for proteinname, number in count_coli_proteins.items():
        labels_chart_coli.append(proteinname)
        count_chart_coli.append(number)
    
    #rest proteins
    for proteinname, number in count_rest_proteins.items():
        labels_chart.append(proteinname)
        count_chart.append(number)

    return count_chart, labels_chart, count_chart_human, labels_chart_human, count_chart_coli, labels_chart_coli

def create_bar_chart():
    general_name, other_names, organisms = categorization()
    human_proteins, coli_proteins, rest_proteins = divideByOrganism(general_name, organisms)
    count_chart, labels_chart, count_chart_human, labels_chart_human, count_chart_coli, labels_chart_coli = labelChart(general_name, human_proteins, coli_proteins, rest_proteins)
    
    #create bar chart
    fig = go.Figure()
    #fig = make_subplots(rows=1, cols=3, subplot_titles=['All Organisms', 'Other Proteins', 'Homo Sapiens Proteins', 'E.coli Proteins'])

    #add traces
    fig.add_trace(go.Bar(
            x=count_chart,
            y=labels_chart,
            orientation='h',
            name='other proteins',
            marker_color = 'blue'))
            #row=1, col=1)
    
    fig.add_trace(go.Bar(
            x=count_chart_human,
            y=labels_chart_human,
            orientation='h',
            name='Homo Sapiens proteins',
            marker_color = "red"))
            #row=1, col=2)
    
    fig.add_trace(go.Bar(
            x=count_chart_coli,
            y=labels_chart_coli,
            orientation='h',
            name='E.coli proteins',
            marker_color = 'orange'))
            #row=1, col=3)
    
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
    ], xaxis_range=[0,25], barmode='stack', hovermode="x unified")

    chart_data = pio.to_json(fig)

    #return the dictionary
    return chart_data 