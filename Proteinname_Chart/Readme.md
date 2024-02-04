# Protein Family Name

This Python script contains functions to generate interactive visualization for protein analysis using Plotly.

## Functions

### `categorization(selected_species)`

This function summarizes the proteins according to general enzyme groupings. It takes one parameter: 
- `selected_species`: List of selected species for filterin the data.

Only proteins that belong to the selected species are used as data. 

### `divideByOrganism(general_name, organisms)`

To include a selection menu within the plot, this function categorises the selected proteins in three cetegories: 
- `human_proteins`
- `coli_proteins`
- `rest_proteins`
It takes two parameters:
- `general_name`: List of protein family names for all selected proteins. 
- `organisms`: List of species name for all selected proteins.

The result are three lists containing the proteins sorted by the three species. 

### `labelChart(general_name, human_proteins, coli_proteins, rest_proteins, count_others)`

This function summarizes the proteins according to general enzyme groupings. It takes one parameter: 
- `general_name`: List of protein family names for all selected proteins. 
- `human_proteins`: List of protein family names for all selected proteins, which species is human. 
- `coli_proteins`: List of protein family names for all selected proteins, which species is E.coli. 
- `rest_proteins`: List of protein family names for all selected proteins, which species is neither human nor E.coli. 
- `count_others`: Dictionary containing protein names and respective number for all selected proteins that are part of category `Other`. 

For each trace (human, E.coli, rest) this function computes two lists. The first one (`count`) includes the number of 
protein family names for each name. The second one (`hovertext`) contains the hovertext.
The labels for each trace are equal to get the same y-axis for each trace. 

### `create_bar_chart(selected_species)`

This function creates the final bar chart. It takes one parameter: 
- `selected_species`: List of selected species for filterin the data.

It makes use of the other functions to create a protein bar chart. It includes three traces to show only human proteins, only E.coli
proteins, the rest proteins or all proteins independent of the other charts within the website. 

## Example Usage

```python
# Example usage of plot_bubble_chart
bar_chart = create_bar_chart(selected_species)
