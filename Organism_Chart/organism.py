import matplotlib.pyplot as plt
from io import BytesIO
import base64
import pandas as pd
from collections import Counter
from pathlib import Path
import numpy as np
import seaborn as sns

def create_pie_chart():
    # data for the pie chart
    root_folder = Path(__file__).parents[1]
    my_path = root_folder / "Database/fetched_data.csv"

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
    fig, ax = plt.subplots(figsize=(12, 5), subplot_kw=dict(aspect="equal"))

    wedges, percentage, text = ax.pie(count_chart, colors=sns.color_palette("Paired"), autopct='%1.2f%%', startangle=-60, textprops={'fontsize': 6})

    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    kw = dict(arrowprops=dict(arrowstyle="-"),
          bbox=bbox_props, zorder=0, va="center")

    # add labels
    for i, p in enumerate(wedges):
        angle_chart = (p.theta2 - p.theta1)/2. + p.theta1
        y = np.sin(np.deg2rad( angle_chart))
        x = np.cos(np.deg2rad( angle_chart))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = "angle,angleA=0,angleB={}".format( angle_chart)
        kw["arrowprops"].update({"connectionstyle": connectionstyle})
        ax.annotate(labels_chart[i], xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),
                horizontalalignment=horizontalalignment, **kw)

    # plot is saved in BytesIO object
    img_io = BytesIO()
    plt.savefig(img_io, format='png')
    img_io.seek(0)
    plt.close()

    # BytesIO object is transformed to a base64-encoded string
    img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')

    return img_base64