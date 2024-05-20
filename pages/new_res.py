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

data = dict(
	labels = ["Topical keywords","Vulnerable populations","Novel treatments","Mental health","Children and adolescents","Migrant workers","People living with HIV (TB treatment)","Psychiatric patients (depression, anxiety, trauma)","Individuals in correctional settings (COVID-19 outbreaks)","Antidepressants for Long COVID","ZOom Delivered Intervention Against Cognitive decline (ZODIAC)","Citicoline for COVID-19 pneumonia (SCARLET trial)","Telehealth services","Post-traumatic growth of critical care nurses", "Impact of COVID-19 on mental health (Finnish youth, adolescents, psychiatric patients)","Mental health after COVID-19 pandemic","Adolescent mental health","Workplace violence against healthcare workers"],
	parents= ["","Topical keywords","Topical keywords","Topical keywords","Vulnerable populations","Vulnerable populations","Vulnerable populations","Vulnerable populations","Vulnerable populations","Novel treatments","Novel treatments","Novel treatments","Novel treatments","Mental health","Mental health","Mental health","Mental health","Mental health"],
	values=[15,10,10,10,1,1,1,1,1,1,1,1,1,1,1,1,1,1])

content_style={
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem"}

content = html.Div(id="page", style=content_style)

fig = px.sunburst(
    data,
    names='labels',
    parents='parents',
    values='values',
)

layout = html.Div([
	html.H1(children='Novel COVID-19 research', style = {'textAlign':'Center'}),
	dcc.Graph(
        id='keywords',
        figure=fig, style={'margin-left':'2px', 'margin-top':'2px','width': '90vh', 'height': '90vh'})
])