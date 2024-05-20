from dash import Dash, html, dash_table, dcc, Input, Output, callback
import dash
import dash_ag_grid as dag
from google.cloud import bigquery
import plotly.express as px
from plotly import graph_objects as go
import numpy as np
import dash_bootstrap_components as dbc
from call_GBQ import run_query
import pandas as pd

dash.register_page(__name__)

fund_query = ('SELECT `covid-19-dimensions-ai.data.grid`.name, '
  '`covid-19-dimensions-ai.data.grants`.funder_org, '
  'SUM(`covid-19-dimensions-ai.data.grants`.funding_usd) AS amt '
  'FROM `covid-19-dimensions-ai.data.grants` '
  'LEFT JOIN `covid-19-dimensions-ai.data.grid` '
  'ON `covid-19-dimensions-ai.data.grid`.id= `covid-19-dimensions-ai.data.grants`.funder_org '
  'GROUP BY `covid-19-dimensions-ai.data.grid`.name,`covid-19-dimensions-ai.data.grants`.funder_org '
  'ORDER BY amt DESC')

df_funds = run_query(fund_query)


content_style={
    "margin-left": "18rem",
    "margin-right": "18rem",
    "padding": "2rem 1rem"}

content = html.Div(id="page", style=content_style)    

layout = html.Div([content,
	html.H1(children='Funding COVID-19 Research', style = {'textAlign':'Center'}),
	dash_table.DataTable(data=df_funds.to_dict('records'), page_size=25)
	])    