# Protein Species Distribution

This Python script contains functions to generate interactive visualization for protein analysis using Plotly.

## Functions

### `speciesIntoOrganism(selected_species)`

This function provides a list with all selected species. It takes one parameter: 
- `selected_species`: List of selected species for filterin the data-

The provided list of species is used to highlight them within the pie chart. 

### `create_pie_chart(selected_species, highlight=0.2)`

This function generates a pie chart to visualize protein data, especially different species. It takes two parameters:
- `selected_species`: List of selected species for filtering the data.
- `highlight`: Value for how much the pieces are highlighted. 

The function filters only sequences with chain `A` to visualise exactly 89 proteins. 
Furthermore, the hovertext including the exact percentage is implemented. The final pie chart is drawn using the highlighted
species of the other function (`spciesIntoIrganism`). 

## Example Usage

```python
# Example usage of plot_bubble_chart
pie_chart_species = create_pie_chart(protein_data, selected_species)
