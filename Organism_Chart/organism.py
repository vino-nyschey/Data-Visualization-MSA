import pandas as pd
from collections import Counter
from pathlib import Path
import plotly.graph_objects as go
import plotly.io as pio
from ipywidgets import Output, VBox


def create_pie_chart():
    # data for the pie chart
    root_folder = Path(__file__).parents[1]
    my_path = root_folder / "Database/fetched_data.csv"

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
        if number > threshold * total_count: 
            labels_chart.append(f"{organism.capitalize()} ({number})")
            count_chart.append(number)
        else: # percentage below threshold -> group together in category 'other'
            total_other = total_other + number   
            organisms_other.append(organism.capitalize())
            count_other.append(number)
    labels_chart.append(f"{'Other Organisms'} ({total_other})")
    count_chart.append(total_other)
    
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
                                 textinfo='label',
                                 hoverinfo='text',
                                 hovertext=hovertext)])
    fig.update_traces(textposition='outside', selector=dict(type='pie')) #labels outside chart
    fig.update(layout_showlegend=False) #no legend

    chart_data = pio.to_json(fig)

    return chart_data