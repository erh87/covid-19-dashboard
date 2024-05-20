from dash import Dash, html, dash_table, dcc, Input, Output, callback
import dash
import dash_ag_grid as dag
from google.cloud import bigquery
import plotly.express as px
from plotly import graph_objects as go
import numpy as np
import dash_bootstrap_components as dbc
from call_GBQ import run_query
from dash_bootstrap_templates import load_figure_template

app = Dash(__name__,external_stylesheets=[dbc.themes.LUX],use_pages=True)

load_figure_template('LUX')

app.layout = html.Div([
    html.H1('COVID-19 Data in Dimensions AI'),
    html.Div([
        html.Div(
            dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
        ) for page in dash.page_registry.values()
    ]),
    dash.page_container
])

app.run_server(debug=True, use_reloader=True)

if __name__ == '__main__':
    app.run(debug=True)