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

res_query = ('SELECT `covid-19-dimensions-ai.data.grid`.name AS Institution, `covid-19-dimensions-ai.data.grid`.address.country as Country,`covid-19-dimensions-ai.data.grid`.address.city as City, TO_JSON_STRING(`covid-19-dimensions-ai.data.grid`.types) AS t, count(r) as c '
    'FROM (SELECT research_orgs FROM '
    '`covid-19-dimensions-ai.data.publications` '
    'WHERE ("COVID-19 Vaccines" IN UNNEST(mesh_headings))), UNNEST(research_orgs) as r '
    'LEFT JOIN  `covid-19-dimensions-ai.data.grid` ON '
    '`covid-19-dimensions-ai.data.grid`.id= r '
    'GROUP BY Institution,Country,City,t '
    'ORDER BY c DESC '
    'LIMIT 100')

all_query = ('SELECT `covid-19-dimensions-ai.data.grid`.name AS Institution, `covid-19-dimensions-ai.data.grid`.address.country as Country,`covid-19-dimensions-ai.data.grid`.address.city as City, TO_JSON_STRING(`covid-19-dimensions-ai.data.grid`.types) AS t, count(r) as c '
    'FROM (SELECT research_orgs FROM '
    '`covid-19-dimensions-ai.data.publications`), UNNEST(research_orgs) as r '
    'LEFT JOIN  `covid-19-dimensions-ai.data.grid` ON '
    '`covid-19-dimensions-ai.data.grid`.id= r '
    'GROUP BY Institution,Country,City,t '
    'ORDER BY c DESC '
    'LIMIT 100')

df_res = run_query(res_query)
df_all = run_query(all_query)

df_res["full_loc"] = df_res.apply(lambda row: row.City + ", " +row.Country, axis=1)
inst_coor = pd.read_csv("coords.tsv",sep="\t")

df_res = df_res.replace(to_replace={'["Education"]':'Education','["Government"]':'Government','["Healthcare"]':'Healthcare','["Facility"]':'Facility','["Nonprofit"]':'Nonprofit'})
df_all = df_all.replace(to_replace={'["Education"]':'Education','["Government"]':'Government','["Healthcare"]':'Healthcare','["Facility"]':'Facility','["Nonprofit"]':'Nonprofit'})

content_style={
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem"}

content = html.Div(id="page", style=content_style)

df_res = df_res.rename({'t':"Institution type",'c':"Papers published"},axis=1)
df_all = df_all.rename({'t':"Institution type",'c':"Papers published"},axis=1)

df_coords = pd.merge(df_res,inst_coor,how="outer").dropna(how="any")
df_coords["Papers published"] = df_coords["Papers published"].astype(np.int64)


fig = px.scatter_geo(df_coords, lat="lat_coor", lon="lon_coor",color="Institution type",
                     hover_name="Institution", size="Papers published",
                     projection="natural earth")    

layout = html.Div([content,
	html.H1(children='Leading COVID-19 Vaccine Research Institutions', style = {'textAlign':'Center'}),
	dcc.Graph(
        id='org_map',
        figure=fig, style={'margin-left':'2px', 'margin-top':'2px'}),
	html.H1(children='Leading COVID-19 Research Institutions', style = {'textAlign':'Center'}),
	dash_table.DataTable(style_data={
        'whiteSpace': 'normal',
        'height': 'auto',
    },data=df_all.to_dict('records'), page_size=25,style_table={'width':'75%'})
	])