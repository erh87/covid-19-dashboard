from dash import Dash, html, dash_table, dcc, Input, Output, callback
import dash_ag_grid as dag
import dash
from google.cloud import bigquery
import plotly.express as px
from plotly import graph_objects as go
import numpy as np
import dash_bootstrap_components as dbc
from call_GBQ import run_query
import pandas as pd

dash.register_page(__name__)

trend_q = ('SELECT year,h,COUNT(h) as h_c FROM `covid-19-dimensions-ai.data.publications`, UNNEST(mesh_headings) AS h '
    'GROUP BY h,year '
    'ORDER by year,h_c DESC ')

years_df = run_query(trend_q)

years_df = years_df.rename({"h":"MeSH heading","h_c":"Publication count"},axis=1)


trends_2020 = years_df[years_df["year"]==2020]

trends_2021 = years_df[years_df["year"]==2021]

trends_2022 = years_df[years_df["year"]==2022]

trends_2023 = years_df[years_df["year"]==2023]


fig1 = px.bar(trends_2020[:25],x="MeSH heading",y="Publication count", title="Popular MeSH Headings in 2020")
fig2 = px.bar(trends_2021[:25],x="MeSH heading",y="Publication count", title="Popular MeSH Headings in 2021",color_discrete_sequence=["red"])
fig3 = px.bar(trends_2022[:25],x="MeSH heading",y="Publication count", title="Popular MeSH Headings in 2022",color_discrete_sequence=["green"])
fig4 = px.bar(trends_2023[:25],x="MeSH heading",y="Publication count", title="Popular MeSH Headings in 2023",color_discrete_sequence=["purple"])

layout = html.Div([
	html.H1(children='Trends in COVID-19 Research', style = {'textAlign':'Center'}),
	dcc.Graph(
        id='sub1',
        figure=fig1, style={'margin-left':'7px', 'margin-top':'7px'})
	])