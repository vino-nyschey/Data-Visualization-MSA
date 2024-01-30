import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def plot_bubble_chart(data, selected_species=None):
    # Convert 'Discovered Year' to integer
    data['Discovered Year'] = pd.to_numeric(data['Discovered Year'], errors='coerce')
    data = data[data['Sequence ID'].str.split(':').str[1] != 'P'] # delete sequence with chain P
    data = data[data['Sequence ID'].str.split(':').str[1] != 'Q'] # delete sequence with chain Q

    # Filter data based on selected species
    if selected_species:
        data = data[data['Species Name'].isin(selected_species)]
    
    # color map
    unique_proteins = data['Protein Family'].unique()
    color_map = {protein: px.colors.qualitative.Plotly[i % 10] for i, protein in enumerate(unique_proteins)}

    # Create a bubble chart with Sequence ID on the x-axis
    fig = px.scatter(data, x='Sequence ID', y='Discovered Year', 
                     color='Protein Family',  # Differentiate by Protein Family
                     color_discrete_map=color_map,
                     size='No. of Chains',
                     opacity=0.7,  # Set default opacity
                     labels={'x': 'Sequence ID', 'y': 'Discovered Year'},
                     title='Protein Discovered Years',
                     template='plotly', height=500,
                     hover_name='Protein Name')  # Specify the hover information here

    # Sort x-axis (Sequence ID) in ascending order
    fig.update_xaxes(categoryorder='array')

    # Add legends
    fig.update_layout(showlegend=True)

    return fig

def plot_pie_chart(data, selected_species=None):
    # Filter data based on selected species
    if selected_species:
        data = data[data['Species Name'].isin(selected_species)]
        data = data[data['Sequence ID'].str.split(':').str[1] == 'A']
    else: 
         data = data[data['Sequence ID'].str.split(':').str[1] == 'A']

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