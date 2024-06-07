from dash import Dash, html, dash_table, dcc, Input, Output, callback
import dash
import dash_ag_grid as dag
from google.cloud import bigquery
import plotly.express as px
from plotly import graph_objects as go
import numpy as np
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

def main():
	app = Dash(__name__,external_stylesheets=[dbc.themes.LUX],use_pages=True)

	content_style={
	    "margin-left": "18rem",
	    "margin-right": "18rem",
	    "padding": "2rem 1rem"}

	content = html.Div(id="page", style=content_style)    

	layout = html.Div([content,
		html.H1(children='Funding COVID-19 Research', style = {'textAlign':'Center'}),
		dash_table.DataTable(data=df_funds.to_dict('records'), page_size=25)
		])    

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

def topOrgs():
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

def topFunders():

def topPubs():

def trendsYearly():

def newTopics():

	data = dict(
	labels = ["Topical keywords","Vulnerable populations","Novel treatments","Mental health","Children and adolescents","Migrant workers","People living with HIV (TB treatment)","Psychiatric patients (depression, anxiety, trauma)","Individuals in correctional settings (COVID-19 outbreaks)","Antidepressants for Long COVID","ZOom Delivered Intervention Against Cognitive decline (ZODIAC)","Citicoline for COVID-19 pneumonia (SCARLET trial)","Telehealth services","Post-traumatic growth of critical care nurses", "Impact of COVID-19 on mental health (Finnish youth, adolescents, psychiatric patients)","Mental health after COVID-19 pandemic","Adolescent mental health","Workplace violence against healthcare workers"],
	parents= ["","Topical keywords","Topical keywords","Topical keywords","Vulnerable populations","Vulnerable populations","Vulnerable populations","Vulnerable populations","Vulnerable populations","Novel treatments","Novel treatments","Novel treatments","Novel treatments","Mental health","Mental health","Mental health","Mental health","Mental health"],
	values=[15,10,10,10,1,1,1,1,1,1,1,1,1,1,1,1,1,1])

if __name__ == '__main__':
    app.run(debug=True)