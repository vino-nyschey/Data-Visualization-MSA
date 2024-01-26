import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def plot_bubble_chart(data, selected_species=None):
    # Convert 'Discovered Year' to integer
    data['Discovered Year'] = pd.to_numeric(data['Discovered Year'], errors='coerce')

    # Filter data based on selected species
    if selected_species:
        data = data[data['Species Name'].isin(selected_species)]
        data = data[data['Organism'].isin(selected_species)]

    # Create a bubble chart with Sequence ID on the x-axis
    fig = px.scatter(data, x='Sequence ID', y='Discovered Year', 
                     color='Protein Family',  # Differentiate by Protein Family
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

     # create hovertext
    protein_counts = data['Protein Family'].value_counts()
    print(protein_counts)
    total_count = sum(protein_counts.values) # total number of organisms
    hovertext = []
    labels_chart = []
    for name, number in zip(protein_counts.index, protein_counts.values):
            hovertext.append(f"{name.capitalize()} ({number})<br> {number/total_count:.2%}")
            labels_chart.append(f"{name.capitalize()} ({number})")
      
    # Create a bar chart with the count of occurrences for each Protein Family
    fig = go.Figure(data=[go.Pie(labels=labels_chart,
                                 values=protein_counts.values,
                                 textinfo='label',
                                 hoverinfo='text',
                                 hovertext=hovertext
                                 )])
    fig.update_traces(textposition='outside', selector=dict(type='pie')) #labels outside chart
    fig.update(layout_showlegend=False) #no legend

    return fig