import base64
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import flask
import io
import json
import pandas as pd
import numpy as np
import plotly
import plotly.graph_objs as go

app = dash.Dash()

app.scripts.config.serve_locally = True
# app.css.config.serve_locally = True

# TODO: Guest list data should only be in the displayed table (No global state!)
NUM_TABLES = 15
GUEST_LIST_INPUT = pd.read_csv('example/guestlist.csv')
GUEST_LIST_INPUT['friends'] = ''
NUM_GUESTS = len(GUEST_LIST_INPUT)
GUESTS_PER_TABLE = NUM_GUESTS // NUM_TABLES
NUM_LEFTOVER_GUESTS = NUM_GUESTS % NUM_TABLES
GUEST_LIST_INPUT['Table'] = 1 + np.arange(0, NUM_GUESTS) // (GUESTS_PER_TABLE + 1 if NUM_LEFTOVER_GUESTS else 0)
GUEST_LIST_INPUT['Table'] = GUEST_LIST_INPUT['Table'].apply(str)


app.layout = html.Div([
    html.H4('Guest List'),
    dt.DataTable(
        rows=GUEST_LIST_INPUT.to_dict('records'),

        # optional - sets the order of columns
        # columns=sorted(DF_GAPMINDER.columns),
        row_selectable=True,
        filterable=True,
        sortable=True,
        selected_row_indices=[],
        id='guest-list'
    ),
    html.Div(id='Sorter'),
    html.Button(id='button-friend', n_clicks=0, children='Make friends'),
    html.A('Download CSV', id='my-link'),
    dcc.Graph(
        id='graph-guest-sorter'
    ),
], className='container')



# TODO: Callback for button
# @app.callback(
#     Output('guest-list', 'selected_row_indices'),
#     [Input('submit-button', 'n_clicks')],
#     [State('guest-list', 'selected_row_indices')])
# )
# def

@app.callback(
    Output('guest-list', 'selected_row_indices'),
    [Input('graph-guest-sorter', 'clickData')],
    [State('guest-list', 'selected_row_indices')])
def update_selected_row_indices(clickData, selected_row_indices):
    if clickData:
        for point in clickData['points']:
            if point['pointNumber'] in selected_row_indices:
                selected_row_indices.remove(point['pointNumber'])
            else:
                selected_row_indices.append(point['pointNumber'])
    return selected_row_indices


@app.callback(
    Output('graph-guest-sorter', 'figure'),
    [Input('guest-list', 'rows'),
     Input('guest-list', 'selected_row_indices')])
def update_figure(rows, selected_row_indices):
    df = pd.DataFrame(rows)

    for tableNum, tableGroup in df.groupby('Table'):
        lg = len(tableGroup)
        tableNum = int(tableNum)
        df.loc[tableGroup.index, 'x'] = tableNum // 2
        df.loc[tableGroup.index, 'y'] = tableNum % 2 + .9 * np.arange(lg)/float(lg)

    return {
        'data': [go.Scatter(
            x=df['x'],
            y=df['y'],
            text=[n[0:10] for n in df['Guest Name']],
            customdata=df.index,
            mode='markers+text',
            textposition='middle right',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'},
            },
            selectedpoints=selected_row_indices,
            selected={
                'marker': {
                    'color': 'rgba(255, 0, 0, 1.)',
                }
            },
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


@app.callback(Output('my-link', 'href'), [Input('guest-list', 'rows')])
def update_link(rows):
    df = pd.DataFrame(rows)

    buffer = io.StringIO()  #creating an empty buffer
    df.to_csv(buffer, index=False)  #filling that buffer
    buffer.seek(0) #set to the start of the stream
    dfEncoded = base64.b64encode(buffer.getvalue().encode('utf-8'))
    buffer.close()
    return '/dash/urlToDownload3?value=' + dfEncoded.decode("utf-8")


@app.server.route('/dash/urlToDownload3')
def download_csv():
    value = flask.request.args.get('value')

    mem = io.BytesIO()
    mem.write(base64.b64decode(value))
    mem.seek(0)
    file = flask.send_file(mem,
                           mimetype='text/csv',
                           attachment_filename='downloadFile.csv',
                           as_attachment=True)
    return file



app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

if __name__ == '__main__':
    app.run_server(debug=True)
