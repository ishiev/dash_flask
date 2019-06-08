import warnings
# Dash configuration
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
from flask_login import current_user
import pandas as pd

from server import app

warnings.filterwarnings("ignore")
def create_df():
    df = pd.DataFrame([x.__dict__.values() for x in current_user.actions],
                 columns=current_user.actions[0].__dict__.keys())
    if not df.empty:
        return df
    else:
        return pd.DataFrame()

# Create success layout
layout = html.Div(children=[
    dcc.Location(id='url_login_success', refresh=True),
    html.Div(
        className="container",
        children=[
            html.Div(
                html.Div(
                    className="row",
                    children=[
                        html.Div(
                            className="ten columns",
                            children=[
                                html.Br(),
                                html.Div('Login successfull'),
                            ]
                        ),
                        html.Div(
                            className="two columns",
                            # children=html.A(html.Button('LogOut'), href='/')
                            children=[
                                html.Br(),
                                html.Button(id='back-button', children='Go back', n_clicks=0)
                            ]
                        )
                    ]
                )
            )
        ]
    ),
    html.Br(),
    html.P('Example graph'),
    html.Br(),
    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    ),
    # dash_table.DataTable(
    #     id='Actions table',
    #     columns=current_user.actions[0].__dict__.keys() if current_user else [],
    #     data=[x.__dict__ for x in current_user.actions] if current_user else [],
    # ),
    html.Br(),
    html.P('Times login in.'),
    html.Br(),
    html.Div([
        html.Div(id='my-div'),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Button(id='update-button', children='Update', n_clicks=0)
    ])
])


# Create callbacks
@app.callback(Output('url_login_success', 'pathname'),
              [Input('back-button', 'n_clicks')])
def logout_dashboard(n_clicks):
    if n_clicks > 0:
        return '/'

@app.callback(Output('my-div', 'children'),
              [Input('update-button', 'n_clicks')])
def logout_dashboard(n_clicks):
    if n_clicks > 0:
        return html.Br(), str([list(x.__dict__.values())[1].strftime("%d-%b-%Y (%H:%M:%S)") for x in current_user.actions])
