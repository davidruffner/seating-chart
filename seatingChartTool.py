import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import json
import pandas as pd
import numpy as np
import plotly
import plotly.graph_objs as go

app = dash.Dash()

app.scripts.config.serve_locally = True
# app.css.config.serve_locally = True

NUM_TABLES = 15
GUEST_LIST = pd.read_csv('example/people.csv')
NUM_GUESTS = len(GUEST_LIST)
GUESTS_PER_TABLE = NUM_GUESTS // NUM_TABLES
NUM_LEFTOVER_GUESTS = NUM_GUESTS % NUM_TABLES
GUEST_LIST['Table'] = 1 + np.arange(0, NUM_GUESTS) // (GUESTS_PER_TABLE + 1 if NUM_LEFTOVER_GUESTS else 0)



app.layout = html.Div([
    html.H4('Guest List'),
    dt.DataTable(
        rows=GUEST_LIST.to_dict('records'),

        # optional - sets the order of columns
        # columns=sorted(DF_GAPMINDER.columns),
        row_selectable=True,
        filterable=True,
        sortable=True,
        selected_row_indices=[],
        id='guest-list'
    ),
    html.Div(id='Sorter'),
    dcc.Graph(
        id='graph-guest-sorter'
    ),
], className='container')


# @app.callback(
#     Output('guestList', 'selected_row_indices'),
#     [Input('graph-gapminder', 'clickData')],
#     [State('guestList', 'selected_row_indices')])
# def update_selected_row_indices(clickData, selected_row_indices):
#     if clickData:
#         for point in clickData['points']:
#             if point['pointNumber'] in selected_row_indices:
#                 selected_row_indices.remove(point['pointNumber'])
#             else:
#                 selected_row_indices.append(point['pointNumber'])
#     return selected_row_indices
#
#
@app.callback(
    Output('graph-guest-sorter', 'figure'),
    [Input('guest-list', 'rows'),
     Input('guest-list', 'selected_row_indices')])
def update_figure(rows, selected_row_indices):
    df = pd.DataFrame(rows)

    for tableNum, tableGroup in df.groupby('Table'):
        lg = len(tableGroup)
        df.loc[tableGroup.index, 'x'] = tableNum // 2
        df.loc[tableGroup.index, 'y'] = tableNum % 2 + .9 * np.arange(lg)/float(lg)
        df.loc[tableGroup.index]

    return {
        'data': [go.Scatter(
            x=df['x'],
            y=df['y'],
            text=[n[0:10] for n in df['Guest Name']],
            customdata=df['friend1'],
            mode='markers+text',
            textposition='middle right',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'showgrid': False,
                'zeroline': False,
                'showticklabels': False,
            },
            yaxis={
                'showgrid': False,
                'zeroline': False,
                'showticklabels': False,
            },
            margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
            height=450,
            hovermode='closest'
        )
    }


app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

if __name__ == '__main__':
    app.run_server(debug=True)
