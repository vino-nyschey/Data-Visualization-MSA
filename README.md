## Project: Visualizing Protein Sequences And Analysis

### Introduction/ Overview
With the rapid development of high-throughput techniques, biologists are faced with an ever growing volume of protein sequence data in multiple different data banks. Deriving information and gaining knowledge about their functions, structures, features and volution is imperative and the goal.
This project aims to facilitate the anaylsis of multiple protein sequences using different visualisation techniques, to expedite the overall analysis process.

### Getting Started / Installation 
0. make sure that you have flask and python installed (download other extensions as required in terminal)
1. Clone repository to your local machine
2. make sure all necessary packages have been installed
3. run python3 website.py or python website.py (depending on version)

```
pip install flask
   
git clone git@github.com:gvarul/Data-Visualization-MSA.git
  
cd Data-Visualization-MSA
   
python website.py 
```

Copy the http code into chosen browser (Safari and Firefox work best)

### Data Source 
The dataset, in form of a fasta file, used for this project is available on Ilias (private uni project).
'protein_seqeunce_analysis_lpt.fasta'
The file consists of 89 Protein Sequences.

### Navigating the website 
#### First Page 
Table of Protein Data. Including additional information: 
<img width="1400" alt="Screenshot 2024-02-04 at 14 11 43" src="https://github.com/gvarul/Data-Visualization-MSA/assets/116247345/8a14eb02-98d1-422b-8c7b-1f45d5e747f2">
More detailed overview by selecting "Details" button for a single protein: 


#### Charts/Visualisations
1) Bubble Chart:
   Year of discovery for each protein.
   
> Function: `plot_bubble_chart(data, selected_species)`

This function generates a bubble chart to visualize protein data. It takes two parameters:
- `data`: DataFrame containing protein data.
- `selected_species`: List of selected species for filtering the data.

The function converts the 'Discovered Year' column to integers, filters the data based on selected species, and generates a bubble chart with Sequence ID on the x-axis, Discovered Year on the y-axis, and Protein Family as the color-coded bubbles. Additional features include sizing bubbles by the number of chains and providing hover information.

2) Pie Charts:
   
   2.1)
   Protein Family Name Distribution
    > Function: `plot_pie_chart(data, selected_species)`

This function generates a pie chart to visualize protein data. It takes two parameters:
- `data`: DataFrame containing protein data.
- `selected_species`: List of selected species for filtering the data.

The function filters the data based on selected species and generates a pie chart representing the count of occurrences for each Protein Family. Each slice of the pie chart represents a Protein Family, with the size of the slice proportional to the count. Hover information is provided to display the count and percentage of each Protein Family.

   2.2) 
   Protein Species Distribution
   > Function: create_pie_chart(selected_species, highlight=0.2)

Following the same principles as above. Each Protein belonging to which species is shown. Hover function enables seeing additional information, that is not immediately obvious.

3) Bar Chart:
   
    Protein Family Name
   
   > Function:create_bar_chart(selected_species)
   
Protein families with their associated number of proteins displayed. Independent of the other charts, you can select different species and only display them in the plot.

   
#### MSA


#### Extras
In the files `Database` and `Fetch-AA-info` are additional ReadMe's describing preprocessing and data handling. 




