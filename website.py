from flask import Flask, render_template, redirect, url_for
from Organism_Chart.organism import create_pie_chart
from Proteinname_Chart.proteinname import create_bar_chart
  
app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
    return redirect(url_for('base'))

@app.route('/base')
def base():
    return render_template('base.html')

@app.route('/Organism_Chart')
def organism_plot(): 
    chart = create_pie_chart()
    print(chart)
    return render_template('index_organism.html', chart_data=chart)

@app.route('/Proteinname_Chart')
def proteinname_plot(): 
    chart = create_bar_chart()
    print(chart)
    return render_template('index_proteinname.html', chart_data=chart)

if __name__ == '__main__':
    app.run(debug=True)