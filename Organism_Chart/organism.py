import pandas as pd
from collections import Counter
from pathlib import Path
import plotly.graph_objects as go
import plotly.io as pio

def speciesIntoOrganism(selected_species): 
    highlighted_species = []
    for sp in selected_species: 
        if sp.lower() == "bacillus sp.": 
            highlighted_species.append("Bacillus subtilis")
        elif sp.lower() == "other sp.": 
            highlighted_species.append("Other Organisms")
            highlighted_species.append("Bos taurus")
            highlighted_species.append("Rattus norvegicus")
            highlighted_species.append("Saccharomyces cerevisiae")
        elif sp.lower() == "candida sp.": 
            highlighted_species.append("Candida rugosa")
        elif sp.lower() == "escherichia coli.": 
            highlighted_species.append("Escherichia coli")
        else: 
            highlighted_species.append(sp)
    return highlighted_species
        
def create_pie_chart(selected_species=None, highlight=0.2):
    # data for the pie chart
    root_folder = Path(__file__).parents[1]
    my_path = root_folder / "Database/fetched_data.csv"
    print(selected_species)
    data =  pd.read_csv(my_path)
    data_filtered = data[data['Sequence ID'].str.split(':').str[1] == 'A'] # to get each protein once independent on how many chains it has
    organisms = data_filtered['Organism']
    count_organism = Counter(organisms) # Counter({'Organism 1': 5, ...})

    labels_chart = []
    count_chart = []
    total_count = sum(count_organism.values()) # total number of organisms
    total_other = 0
    count_other = []
    organisms_other = []
    threshold = 0.02 # threshold to group organisms with less percentage than this threshold

    for organism, number in count_organism.items():
        print(count_organism)
        if number > threshold * total_count: 
            labels_chart.append(f"{organism.capitalize()} ({number})")
            count_chart.append(number)
        else: # percentage below threshold -> group together in category 'other'
            total_other = total_other + number   
            organisms_other.append(organism.capitalize())
            count_other.append(number)
    labels_chart.append(f"{'Other Organisms'} ({total_other})")
    count_chart.append(total_other)
    
    # highlight selected species
    if selected_species is not None: 
        highlighted_species = speciesIntoOrganism(selected_species)
        pull_values = [highlight if any(sp.lower() in element.lower() for sp in highlighted_species) else 0 for element in labels_chart]
        if all(e == 0.2 for e in pull_values): 
            pull_values = 0
    else: 
        pull_values = 0

    # create hovertext
    hovertext = []
    for organism, number in zip(labels_chart, count_chart):
        if "Other Organisms" in organism:
            hovertext.append(f"Other Organisms:<br>" + "<br>".join([f"{org}: {count/total_count:.2%}" for org, count in zip(organisms_other, count_other)]))
        else:
            hovertext.append(f"{organism}<br> {number/total_count:.2%}")

    # create pie chart   
    fig = go.Figure(data=[go.Pie(labels=labels_chart,
                                 values=count_chart,
                                 pull=pull_values,
                                 textinfo='label',
                                 hoverinfo='text',
                                 hovertext=hovertext)])
    fig.update_traces(textposition='outside', selector=dict(type='pie')) #labels outside chart
    fig.update(layout_showlegend=False) #no legend

    chart_data = pio.to_json(fig)

    return chart_data