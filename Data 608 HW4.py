import pandas as pd
import numpy as np

url = 'https://data.cityofnewyork.us/resource/nwxe-4ae8.json'
trees = pd.read_json(url)
#print(trees.head(10))
print(list(trees))
print(trees.groupby(['health', 'boroname', 'spc_common'])[['tree_id']].count())
tree_trim1 = trees.groupby(['health', 'boroname', 'spc_common'])[['tree_id']].count()
print(tree_trim1.unstack())
tree_trim2 = tree_trim1.unstack().unstack()
print(tree_trim2)


import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

trees["boroname"].fillna("Unkown Borough", inplace = True) 
boro_choices = trees['boroname'].unique()
trees["spc_common"].fillna("Unkown Species", inplace = True) 
species_choices = trees['spc_common'].unique()


app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in species_choices],
                value='London plantree'
            ),
            dcc.RadioItems(
                id='xaxis-type',
                options=[{'label': i, 'value': i} for i in boro_choices],
                value='Manhattan',
                labelStyle={'display': 'inline-block'}
            ) 
        ],
        style={'width': '48%', 'display': 'inline-block'}),
      ]),
       dcc.Graph(id='indicator-graphic') 
    ])

@app.callback(
     Output('indicator-graphic', 'figure'),   
     [Input('xaxis-column', 'value'),
     Input('xaxis-type', 'value')])
def update_graph(xaxis_column_name, xaxis_type):
    trees_f = trees[trees['spc_common'] == xaxis_column_name & trees['boroname'] == xaxis_type]
    print(trees_f)
    return {'data': [{'x':trees_f.health.unique(),
                      'y':trees_f.groupby(['health']).count()
                    }],
           }

#if __name__ == '__main__':
#   app.run_server(debug=True)