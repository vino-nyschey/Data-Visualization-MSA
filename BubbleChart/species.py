import pandas as pd
import plotly.express as px

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


def plot_bar_chart(data, selected_species=None):
    # Filter data based on selected species
    if selected_species:
        data = data[data['Species Name'].isin(selected_species)]

    # Create a bar chart with the count of occurrences for each Protein Family
    bar_fig = px.bar(data, y='Protein Family', title='Distribution of Protein for different Species',
                     color='Species Name',
                     labels={'Protein Family': 'Protein Families'},
                     template='plotly', height=400,
                     hover_name='Organism')

    # Add legends
    bar_fig.update_layout(showlegend=True)

    return bar_fig