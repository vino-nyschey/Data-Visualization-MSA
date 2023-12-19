Mind Map: Protein Sequence Analysis By G.V. Arulrajah

[What?]

   - Objective
      - Dealing with a large number of protein data
      - Derive information about proteins
         - Functions, structures, features, evolution

   - Approach
      - Multiple Sequence Aligner (MSA)
         - Compare primary sequences
         - Analyze output for differences, variations, clusters 

    - Phylogenetic Tree 
         - Compare selected sequences for Biological 
         - Analyze output for evolutionary relationships

[Why?]
   - Exponential growth of protein sequences
      - Need for efficient analysis methods

   - Gain knowledge about proteins
      - Functions, structures, features, evolution

   - Communication
      - Visualization accelerates the analysis process
      - Researchers can communicate findings effectively

   - Use of FASTA file (Ilias: protein_sequence_analysis_lpt.fasta)
      - 89 protein sequences for analysis

[How?]
   - Multiple Sequence Aligner (MSA)
      - Compare primary sequences
      - Identify differences and variations

   - Analysis of MSA output
      - Visualize output for faster comprehension
      - Answer specific questions:
         - Any important similarities (common domains)?
         - Do proteins form clusters?
         - Are there evolutionary relationships?

   - Data Source
      - Ilias: protein_sequence_analysis_lpt.fasta
         - 89 protein sequences

   - Potential Analyses
      - Identify common domains
      - Cluster analysis of proteins
      - Explore evolutionary relationships
      - Phylogenetic Tree for similar Protiens

   - Visualization Project
        - Utilize tools for visualizing MSA output
            - Choice of Algoritm 
                - MUSCLE
                - CLUSTAL W 
                - CLUSTAL O
                - TCoffee
            - Choice of Language and Tools 
                - Plotly & Flask 
                - Javascript 
                - R ? (https://m-clark.github.io/webR/intro.html)
        - Similar Tools Standalone Softwares
            - MSA 
                - JalView
                - UGENE
            - Phylogenetic Tree  
                - Figtree
                - UGENE   
        
            

backend
	MSA program
		clustering 
			threshold to hide low count clusters. 
		comparison of our 89 proteins with Protein Database to discover families.  
	Protein domain search via API
		 
frontend 
	visualization of cluster MSAs
		user can select individual Clusters to be displayed. 
		different color choices for visual disabled 
	show with a chart the different protein domain and structures. 
	visualization of phylogenetic tree 
	Show Protein 3D structure. 
		Chimera program 
	Layout of the website 
		Flask (python)

- Insprirational Projects and references
            - https://academic.oup.com/bioinformaticsadvances/article/1/1/vbab009/6345340?login=false
            - https://github.com/thekaplanlab/msabrowser/blob/master/README.md
            - https://visme.co/blog/data-visualization-types/
https://biopython-tutorial.readthedocs.io/en/latest/notebooks/13%20-%20Phylogenetics%20with%20Bio.Phylo.html


