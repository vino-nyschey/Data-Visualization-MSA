# Protein Analysis Visualizer

This Python script contains functions to generate interactive visualizations for protein analysis using Plotly Express and Plotly Graph Objects.

## Functions

### `plot_bubble_chart(data, selected_species)`

This function generates a bubble chart to visualize protein data. It takes two parameters:
- `data`: DataFrame containing protein data.
- `selected_species`: List of selected species for filtering the data.

The function converts the 'Discovered Year' column to integers, filters the data based on selected species, and generates a bubble chart with Sequence ID on the x-axis, Discovered Year on the y-axis, and Protein Family as the color-coded bubbles. Additional features include sizing bubbles by the number of chains and providing hover information.

### `plot_pie_chart(data, selected_species)`

This function generates a pie chart to visualize protein data. It takes two parameters:
- `data`: DataFrame containing protein data.
- `selected_species`: List of selected species for filtering the data.

The function filters the data based on selected species and generates a pie chart representing the count of occurrences for each Protein Family. Each slice of the pie chart represents a Protein Family, with the size of the slice proportional to the count. Hover information is provided to display the count and percentage of each Protein Family.

## Example Usage

```python
# Example usage of plot_bubble_chart
fig_bubble = plot_bubble_chart(protein_data, selected_species)

# Example usage of plot_pie_chart
fig_pie = plot_pie_chart(protein_data, selected_species)
