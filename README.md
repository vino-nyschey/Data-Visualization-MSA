## Project: Visualising Protein Sequences

### Introduction / Overview
With the rapid development of high-throughput techniques, biologists are faced with an ever growing volume of protein sequence data in multiple different data banks. Deriving information and gaining knowledge about their functions, structures, features and volution is imperative and the goal.
This project aims to facilitate the anaylsis of multiple protein sequences using different visualisation techniques, to expedite the overall analysis process.

### Getting Started / Installation 
0. Make sure that you have flask and python installed (download other extensions as required in terminal).
1. Clone repository to your local machine.
2. Make sure all necessary packages have been installed.
3. Run python3 website.py or python website.py (depending on version).

```
pip install -r requirements.txt
   
git clone git@github.com:gvarul/Data-Visualization-MSA.git
  
cd Data-Visualization-MSA
   
python website.py 
```

Copy the code into chosen browser. We recommend Safari and Firefox, which are working best.

### Data Source 
The project is based on a dataset, in form of a fasta file (`protein_sequence_analysis_lpt.fasta`), which is available in `DataSource`. The file consists of 89 Protein Sequences and their respective protein IDs. 

### Using your own FASTA file
Any FASTA file whose headers are PDB chain IDs can be analysed, e.g. `>1AH7:A`, `>1AH7:A|PDBID|CHAIN|SEQUENCE`, `>1AH7_A` or the current RCSB download format `>4HHB_1|Chains A, C|...` (one entry per listed chain).
Either upload it on the first page of the website ("Use your own sequences"), or build the dataset on the command line:

```
python -m Pipeline.build_dataset path/to/sequences.fasta
python website.py
```

The pipeline (`Pipeline/`) reads protein name, organism, engineered flag and deposition year from the local PDB files in `Fetch-AA-info/PDB-Database` or, for all other IDs, from the RCSB PDB API (cached in `datasets/rcsb_cache.json`). It then assigns protein families and species groups (`Database/DatabaseGenerator.py`) and aligns each family with a built-in center-star aligner (Biopython, BLOSUM62).
The result is stored in `datasets/active/` and shown by the website instead of the sample data; "Back to sample dataset" on the first page removes it.
Options: `--offline` (no RCSB requests), `--msa-dir DIR` (use your own pre-aligned files, e.g. from MUSCLE, named `<FAMILY>_align.fasta`), `--out DIR`.

### Navigating the website 
#### First Page 
Table of Protein Data including additional information: 
<img width="1400" alt="Screenshot 2024-02-04 at 14 11 43" src="https://github.com/gvarul/Data-Visualization-MSA/assets/116247345/8a14eb02-98d1-422b-8c7b-1f45d5e747f2">
More detailed overview by selecting "Details" button for a single protein.


#### Charts/Visualisations
Our charts are implemented using [plotly](https://plotly.com/python/). We added additional interactions via buttons between all four charts. 

1) Bubble Chart: Protein Discovery by Year
   
   This plot shows all protein sequences and their respective year of discovery. The size of each bubble corrsponds to its number of chains. 

2) Pie Charts:
   
   2.1) Protein Family Name Distribution

   Each slice of the pie chart represents a Protein Family, with the size of the slice proportional to the count.

   2.2) Protein Species Distribution

   This chart represents the variety of species the proteins belong to. Species with a small percentage are grouped together in the category `Other Species`.

3) Bar Chart: Protein Family Name

   The protein family names are also shown in a bar chart to get a better comparison between different protein family names. Furthermore, this plot differentiates between human proteins, E.coli proteins and other proteins.
   
#### MSA

Proteins are clustered into their respective groups. Output is a MSA for each protein family. 
The [MUSCLE alignment online tool](http://ebi.ac.uk/tools/MSA/muscle/) was used to create the MSA. 
In MSA window you can choose a colour design. Choice between colours used in Clustal, Lesk and a Custom colour palette to accomodate various contrasts.

#### Extras
In the files `BubbleChart`, `Database`, `Fetch-AA-info`, `MSA_FLASK`, `Organism_Chart`, and `Proteinname_Chart` are additional Readme's describing preprocessing and data handling. 




