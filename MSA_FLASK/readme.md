#### Purpose
- `modifiedMSA.py` is a Python script that serves as the backend of the Protein Sequence Alignment Visualization Web App. It handles the routing, data processing, and rendering of HTML templates.
  
#### Dependencies
- Imports necessary libraries such as Flask, os, collections, json, etc.
   
#### Functions
- `get_sequence_details_from_json(json_file_path)`: Loads sequence details from a JSON file.
- `parse_fasta(file_path)`: Parses sequences from a FASTA file.
- `calculate_coverage_consensus(sequences)`: Calculates coverage and consensus percentages.
- Flask Routes:
  - `/`: Renders the index page for selecting a FASTA file.
  - `/visualize`: Processes the selected file and renders the visualization page.

#### HTML Rendering
- Renders HTML templates using Flask's `render_template` function.


#### Purpose
- `visualize.html` is an HTML file responsible for rendering the sequence alignment visualization on the frontend of the web app.

#### Content
- Contains HTML structure, CSS styles, and JavaScript code for generating the sequence alignment matrix plot.
  
#### Features
- Dynamically generates a matrix plot based on the selected color scale (Clustal, Lesk, Custom).
- Provides tooltips for sequence details (Organism, Protein Name, Engineered, Sequence Length, No. of Chains).
- Allows users to switch between different color scales using buttons.
   
#### Functionality
- Fetches data from the Flask backend using Jinja templating.
- Generates a matrix plot with colored amino acids representing the alignment.
- Displays coverage and consensus percentages in the footer row.

Input Data : `prealigned.fasta` with gaps 
`ProteinDatabase` to fetch further information into sequence details.