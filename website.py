# Html

from flask import Flask, render_template
# import already existing files
from Organism_Chart.organism import organism_bp
from Proteinname_Chart.proteinname import proteinname_bp

app = Flask(__name__)

app.register_blueprint(organism_bp, url_prefix='/organism')
app.register_blueprint(proteinname_bp, url_prefix='/proteinname')

if __name__ == '__main__':
    app.run(debug=True)

app = Flask(__name__)