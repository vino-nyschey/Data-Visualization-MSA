import dash_bio as dashbio
from dash import Dash, html, Input, Output, callback
import urllib.request as urlreq

app = Dash(__name__)

# HtML call JavaScript which will inreturn  plot this drop down menu and call the MSAvis.py
# this python file will call the HTML file   
# data should be the individual fasta aligned files 
#data = urlreq.urlopen(
#    'https://git.io/alignment_viewer_p53.fasta'
#).read().decode('utf-8')
# create a placeholder to select aligned files , drop down menu 

# data = something.fasta alignment 

app.layout = html.Div([
    dashbio.AlignmentChart(
        id='my-default-alignment-viewer',
        data=data,
        height=900,
        tilewidth=30,
    ),
    html.Div(id='default-alignment-viewer-output')
])

@callback(
    Output('default-alignment-viewer-output', 'children'),
    Input('my-default-alignment-viewer', 'eventDatum')
)
def update_output(value):
    if value is None:
        return 'No data.'
    return str(value)

data = urlreq.urlopen(
    'https://git.io/alignment_viewer_p53.fasta'
).read().decode('utf-8')


dashbio.AlignmentChart(
    data=data,
    colorscale='hydro',
    conservationcolorscale='blackbody',
    height=900,
    tilewidth=30,
)

if __name__ == '__main__':
    app.run(debug=True)