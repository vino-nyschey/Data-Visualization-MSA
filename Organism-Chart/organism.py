from flask import Flask, render_template
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import pandas as pd
from collections import Counter
from pathlib import Path

app = Flask(__name__)

def create_chart():
    # data for the pie chart
    root_folder = Path(__file__).parents[1]
    my_path = root_folder / "Fetch-AA-info/output_data.csv"

    data =  pd.read_csv(my_path)
    data_filtered = data[data['Sequence ID'].str.split(':').str[1] == 'A'] # to get each protein once independent on how many chains it has
    organisms = data_filtered['Organism']
    count_organism = Counter(organisms) # Counter({'Organism 1': 5, ...})

    labels_chart = []
    count_chart = []
    total_count = sum(count_organism.values()) # total number of organisms
    count_other = 0
    organisms_other = []
    threshold = 0.02 # threshold to group organisms with less percentage than this threshold

    for organism, number in count_organism.items():
        if number > threshold * total_count: 
            labels_chart.append(f"{organism} ({number})")
            count_chart.append(number)
        else: # percentage below threshold -> group together in category 'other'
            count_other = count_other + number   
            organisms_other.append(organism)
    labels_chart.append(f"{'Other Organisms'} ({count_other})")
    count_chart.append(count_other)
    
    # create pie chart
    fig, ax = plt.subplots()
    ax.pie(count_chart, labels=labels_chart, autopct='%1.1f%%', startangle=90, textprops={'fontsize': 8})
    ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular

    # plot is saved in BytesIO object
    img_io = BytesIO()
    plt.savefig(img_io, format='png')
    img_io.seek(0)
    plt.close()

    # BytesIO object is transformed to a base64-encoded string
    img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')

    return img_base64

@app.route('/')
def main():
    pie_chart = create_chart()
    return render_template('index_organism.html', pie_chart=pie_chart)

if __name__ == '__main__':
    app.run(debug=True)