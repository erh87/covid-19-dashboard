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

pub_QUERY = (
    'SELECT altmetrics.score,title.preferred,a.last_name,a.first_name,a.researcher_id FROM `covid-19-dimensions-ai.data.publications`, '
    'UNNEST(authors) AS a '
    'ORDER BY altmetrics.score DESC '
    'LIMIT 10000')

df_pubs= run_query(pub_QUERY)

df_by_auth = df_pubs.dropna(subset=['researcher_id']).groupby("researcher_id")["score"].sum()

df_by_auth= df_by_auth.sort_values(ascending=False)
top_auths = list(df_by_auth.iloc[:15].index)

top_pubs = df_pubs[df_pubs['researcher_id'].isin(top_auths)]

top_5 = pd.DataFrame(df_pubs.preferred.unique())

fig=px.bar(top_pubs,x="researcher_id",y="score",color="preferred",color_discrete_sequence=px.colors.qualitative.Alphabet)
fig.update_layout(xaxis_title="Researcher", yaxis_title="Altmetric Score", showlegend=False,xaxis={'categoryorder':'total descending'})
fig.update_xaxes(tickvals=np.arange(15))

layout = html.Div([
    html.H1(children='Influential researchers', style = {'textAlign':'Center','margin-left':'7px', 'margin-top':'7px'}),
        dcc.Graph(
        id='example-graph',
        figure=fig, style={'margin-left':'7px', 'margin-top':'7px'}),

    html.H1(children='Top publications by Altmetric score', style = {'textAlign':'Center','margin-left':'7px', 'margin-top':'7px'}),

    dash_table.DataTable(style_data={
        'whiteSpace': 'normal',
        'height': 'auto',},data=top_5.to_dict('records'), page_size=5,style_table={'width':'75%'})
])