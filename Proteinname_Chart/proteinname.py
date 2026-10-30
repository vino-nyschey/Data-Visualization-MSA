from collections import Counter
import plotly.graph_objects as go
import plotly.io as pio

from dataset import one_chain_per_protein

# function to categorize the proteins according to general enzyme groupings
def categorization(data, selected_species): 
    # filter data based on selected species
    if selected_species:
        data = data[data['Species Name'].isin(selected_species)]
    data = one_chain_per_protein(data) # to get each protein once independent on how many chains it has

    proteinnames = data['Protein Name']
    organisms = data['Species Name']
    general_name = [] # grouped names of proteins
    other_names = [] # protein names part of category other

    # summarize proteins according to general enzyme groupings
    for proteinname in proteinnames:
        proteinname = str(proteinname)
        if 'LIPASE' in proteinname.upper(): 
            general_name.append('Lipase')
        elif 'KINASE' in proteinname.upper(): 
            general_name.append('Kinase')
        elif 'PHOSPHATASE' in proteinname.upper(): 
            general_name.append('Phosphatase')
        elif 'TRANSFERASE' in proteinname.upper(): 
            general_name.append('Transferase')
        elif 'ESTERASE' in proteinname.upper(): 
            general_name.append('Esterase')
        elif 'HYDROLASE' in proteinname.upper(): 
            general_name.append('Hydrolase')
        elif 'PEPTIDE' in proteinname.upper(): 
            general_name.append('Peptide')
        elif 'PHOSPHORYLASE' in proteinname.upper(): 
            general_name.append('Phosphorylase')
        else: 
            general_name.append('Other')
            other_names.append(proteinname.capitalize()) 

    count_others = Counter(other_names)
    return general_name, count_others, organisms

# function to divide proteins and their protein names according to their organism
def divideByOrganism(general_name, organisms): 
    human_proteins = [] # protein names of human proteins
    coli_proteins = [] # protein names of E.coli proteins
    rest_proteins = [] # protein names of other proteins

    #cdivide proteins according to organism
    for proteinname, organism in zip(general_name, organisms):
       if 'HOMO SAPIENS' == organism:
            human_proteins.append(proteinname)
       elif 'ESCHERICHIA COLI.' == organism: 
           coli_proteins.append(proteinname)
       else: 
           rest_proteins.append(proteinname)

    return human_proteins, coli_proteins, rest_proteins

# function to prepare labels and counts for the final bar chart
def labelChart(general_name, human_proteins, coli_proteins, rest_proteins, count_others): 
    axis_label = ['Esterase', 'Hydrolase', 'Kinase', 'Lipase', 'Other', 'Phosphatase', 'Phosphorylase', 'Transferase']
    # add any further category (e.g. 'Peptide') found in the data so it does not get lost
    axis_label += sorted(set(general_name) - set(axis_label))
    total_count = len(human_proteins) + len(coli_proteins) + len(rest_proteins)

    # counts and hovertexts are built in axis_label order so each hovertext belongs to its bar
    def countsAndHovertext(proteins):
        counts = Counter(proteins)
        count_chart = [counts.get(label, 0) for label in axis_label]
        hovertext = []
        for proteinname, number in zip(axis_label, count_chart):
            if proteinname == "Other":
                hovertext.append(f"Other ({number}):<br>" + "<br>".join([f"{n}: {count/total_count:.2%}" for n, count in count_others.items()]))
            else:
                hovertext.append(f"{proteinname} ({number})<br> {number/total_count:.2%}")
        return count_chart, hovertext

    count_chart_human, hovertext_human = countsAndHovertext(human_proteins) # only human proteins
    count_chart_coli, hovertext_coli = countsAndHovertext(coli_proteins) # only E.coli proteins
    count_chart, hovertext = countsAndHovertext(rest_proteins) # rest bar plot

    return count_chart, count_chart_human, count_chart_coli, hovertext, hovertext_coli, hovertext_human, axis_label

# function to create bar chart (x-axis: number of proteins, y-axis: protein family names)
def create_bar_chart(data, selected_species):
    general_name, count_others, organisms = categorization(data, selected_species)
    human_proteins, coli_proteins, rest_proteins = divideByOrganism(general_name, organisms)
    count_chart, count_chart_human, count_chart_coli, hovertext, hovertext_coli, hovertext_human, axis_label = labelChart(general_name, human_proteins, coli_proteins, rest_proteins, count_others)

    # create bar chart
    fig = go.Figure()
    
    # add traces (human, E.coli, other)
    fig.add_trace(go.Bar(
            x=count_chart,
            y=axis_label,
            orientation='h',
            name='Other Proteins',
            marker_color = '#EF553B',
            hoverinfo='text',
            hovertext=hovertext))
    
    fig.add_trace(go.Bar(
            x=count_chart_human,
            y=axis_label,
            orientation='h',
            name='Homo Sapiens Proteins',
            marker_color = "#636EFA",
            hoverinfo='text',
            hovertext=hovertext_human))
    
    fig.add_trace(go.Bar(
            x=count_chart_coli,
            y=axis_label,
            orientation='h',
            name='E.coli Proteins',
            marker_color = '#00CC96',
            hoverinfo='text',
            hovertext=hovertext_coli))
    
    fig.update_layout(
        xaxis_title="Number of Proteins",  # x-axis label
        yaxis_title="Protein Family",  # y-axis label
        updatemenus=[
            dict(
                x=0, 
                y=1.2,
                active=0,
                    buttons=list([
                        dict(label="All Species",
                            method="update",
                            args=[{"visible": [True, True, True]}]),
                        dict(label="Other Proteins",
                            method="update",
                            args=[{"visible": [True, False, False]}]),
                        dict(label="Homo Sapiens Proteins",
                            method="update",
                            args=[{"visible": [False, True, False]}]),
                        dict(label="E.coli Proteins",
                            method="update",
                            args=[{"visible": [False, False, True]}]),
                    ]),
             )
         ], barmode='stack'
    )

    chart_data = pio.to_json(fig)

    # return the dictionary
    return chart_data 