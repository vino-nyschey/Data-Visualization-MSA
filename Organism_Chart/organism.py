from collections import Counter
import plotly.graph_objects as go
import plotly.io as pio

from dataset import one_chain_per_protein

def create_pie_chart(data, selected_species, highlight=0.2):
    # data for the pie chart
    data_filtered = one_chain_per_protein(data) # to get each protein once independent on how many chains it has
    organisms = data_filtered['Organism']
    count_organism = Counter(organisms) # Counter({'Organism 1': 5, ...})

    labels_chart = []
    count_chart = []
    organisms_chart = [] # organisms belonging to each slice
    total_count = sum(count_organism.values()) # total number of organisms
    total_other = 0
    count_other = []
    organisms_other = []
    threshold = 0.02 # threshold to group organisms with less percentage than this threshold

    for organism, number in count_organism.items():
        if number > threshold * total_count: 
            labels_chart.append(f"{organism.capitalize()} ({number})")
            count_chart.append(number)
            organisms_chart.append({organism.upper()})
        else: # percentage below threshold -> group together in category 'other'
            total_other = total_other + number   
            organisms_other.append(organism.capitalize())
            count_other.append(number)
    if total_other:
        labels_chart.append(f"{'Other Species'} ({total_other})")
        count_chart.append(total_other)
        organisms_chart.append({organism.upper() for organism in organisms_other})
    
    # highlight the slices of the organisms belonging to the selected species
    pull_values = 0
    if selected_species: 
        selected_organisms = set(data_filtered[data_filtered['Species Name'].isin(selected_species)]['Organism'].str.upper())
        pull_values = [highlight if organisms & selected_organisms else 0 for organisms in organisms_chart]
        if all(e == highlight for e in pull_values): 
            pull_values = 0

    # create hovertext
    hovertext = []
    for organism, number in zip(labels_chart, count_chart):
        if "Other Species" in organism:
            hovertext.append(f"Other Species:<br>" + "<br>".join([f"{org}: {count/total_count:.2%}" for org, count in zip(organisms_other, count_other)]))
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