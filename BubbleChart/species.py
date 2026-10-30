import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from dataset import one_chain_per_protein

def plot_bubble_chart(data, selected_species):
    # Convert 'Discovered Year' to integer
    data['Discovered Year'] = pd.to_numeric(data['Discovered Year'], errors='coerce')
    data = data[data['Protein Family'] != 'PEPTIDE']  # delete short peptide chains bound to the proteins

    # Filter data based on selected species
    data = data[data['Species Name'].isin(selected_species)]
    # capitalized family name per row for the hovertext
    data = data.assign(**{'Family Label': data['Protein Family'].fillna('').astype(str).str.capitalize()})
    # color map
    unique_proteins = data['Protein Family'].unique()
    color_map = {protein: px.colors.qualitative.Plotly[i % 10] for i, protein in enumerate(unique_proteins)}
        

    # Erstelle ein Bubble-Chart mit Sequence ID auf der x-Achse
    fig = px.scatter(data, x='Sequence ID', y='Discovered Year',
                     color='Protein Family',  # Differentiate by Protein Family
                     color_discrete_map=color_map,
                     size='No. of Chains',
                     opacity=0.7,  # Set default opacity
                     labels={'x': 'Sequence ID', 'y': 'Discovered Year'},
                     template='plotly', 
                     height=500,
                     hover_name='Protein Name',  # Specify the hover information here
                     custom_data=['Family Label']
                     )

    # capitalize legend labels
    fig.for_each_trace(lambda l: l.update(name=l.name.capitalize()))

    # create hovertext
    fig.update_traces(hovertemplate='<b>%{hovertext}</b>'
                                    '<br><br>Protein Family: %{customdata[0]}'
                                    '<br>Sequence ID: %{x}'
                                    '<br>Discovered Year: %{y}'
                                    '<br>No. of Chains: %{marker.size}'
                                    '<extra></extra>')

    # Sort x-axis (Sequence ID) in ascending order
    fig.update_xaxes(categoryorder='array')

    # Add legends
    fig.update_layout(showlegend=True)

    return fig

def plot_pie_chart(data, selected_species):
    # Filter data based on selected species
    if selected_species:
        data = data[data['Species Name'].isin(selected_species)]
    data = one_chain_per_protein(data) # to get each protein once independent on how many chains it has

    # color map
    unique_proteins = data['Protein Family'].unique()
    color_map = {protein: px.colors.qualitative.Plotly[i % 10] for i, protein in enumerate(unique_proteins)}

    # create hovertext
    protein_counts = data['Protein Family'].value_counts()
    total_count = sum(protein_counts.values) # total number of organisms
    hovertext = []
    labels_chart = []
    for name, number in zip(protein_counts.index, protein_counts.values):
        labels_chart.append(f"{name.capitalize()} ({number})")
        hovertext.append(f"{name.capitalize()} ({number})<br> {number/total_count:.2%}")
      
    # Create a bar chart with the count of occurrences for each Protein Family
    fig = go.Figure(data=[go.Pie(labels=labels_chart,
                                 values=protein_counts.values,
                                 textinfo='label',
                                 hoverinfo='text',
                                 hovertext=hovertext,
                                 )])
    fig.update_traces(marker=dict(colors=[color_map[p] for p in protein_counts.index])) #add color map
    fig.update_traces(textposition='outside', selector=dict(type='pie')) #labels outside chart
    fig.update(layout_showlegend=False) #no legend

    return fig