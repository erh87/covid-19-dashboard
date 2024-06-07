from dash import Dash, html, dash_table, dcc, Input, Output, callback
import dash_ag_grid as dash_ag_grid
import plotly.express as px
from plotly import graph_objects as go
import numpy as np
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import pandas as pd

def topOrgs():

	df_res = pd.read_csv('data/top_vaccine_res_orgs.csv')
	df_all = pd.read_csv('data/top_res_orgs.csv')
	df_res["full_loc"] = df_res.apply(lambda row: row.City + ", " +row.Country, axis=1)
	inst_coor = pd.read_csv("data/coords.tsv",sep="\t")

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

	return(df_coords,df_all)

def topFunders():

	df_funds = pd.read_csv('data/top_funders.csv')

	return(df_funds)

def topPubs():

	df_pubs = pd.read_csv('data/top_pubs.csv')
	df_by_auth = df_pubs.dropna(subset=['researcher_id']).groupby("researcher_id")["score"].sum()

	df_by_auth= df_by_auth.sort_values(ascending=False)
	top_auths = list(df_by_auth.iloc[:15].index)

	top_pubs = df_pubs[df_pubs['researcher_id'].isin(top_auths)]

	top_5 = pd.DataFrame(df_pubs.preferred.unique())

	return(top_pubs,top_5)

def trendsYearly():

	years_df = pd.read_csv('data/trends_yearly.csv')

	years_df = years_df.rename({"h":"MeSH heading","h_c":"Publication count"},axis=1)

	trends_2020 = years_df[years_df["year"]==2020]
	trends_2021 = years_df[years_df["year"]==2021]
	trends_2022 = years_df[years_df["year"]==2022]
	trends_2023 = years_df[years_df["year"]==2023]

	return(trends_2020,trends_2021,trends_2022,trends_2023)

def newTopics():

	topic_data = dict(
	labels = ["Topical keywords","Vulnerable populations","Novel treatments","Mental health","Children and adolescents","Migrant workers","People living with HIV (TB treatment)","Psychiatric patients (depression, anxiety, trauma)","Individuals in correctional settings (COVID-19 outbreaks)","Antidepressants for Long COVID","ZOom Delivered Intervention Against Cognitive decline (ZODIAC)","Citicoline for COVID-19 pneumonia (SCARLET trial)","Telehealth services","Post-traumatic growth of critical care nurses", "Impact of COVID-19 on mental health (Finnish youth, adolescents, psychiatric patients)","Mental health after COVID-19 pandemic","Adolescent mental health","Workplace violence against healthcare workers"],
	parents= ["","Topical keywords","Topical keywords","Topical keywords","Vulnerable populations","Vulnerable populations","Vulnerable populations","Vulnerable populations","Vulnerable populations","Novel treatments","Novel treatments","Novel treatments","Novel treatments","Mental health","Mental health","Mental health","Mental health","Mental health"],
	values=[15,10,10,10,1,1,1,1,1,1,1,1,1,1,1,1,1,1])

	return(topic_data)

def main():

	df_funds = topFunders()
	df_coords,df_all = topOrgs()
	new_topics_df = newTopics()
	trends_2020,trends_2021,trends_2022,trends_2023 = trendsYearly()
	pubs_df,top_5=topPubs()

	print("made it")

	scatter_fig = px.scatter_geo(df_coords, lat="lat_coor", lon="lon_coor",color="Institution type",
		hover_name="Institution", size="Papers published",
		projection="natural earth")

	sun_fig = px.sunburst(new_topics_df,
		names='labels',
		parents='parents',
		values='values')

	bar_2020 = px.bar(trends_2020[:25],x="MeSH heading",y="Publication count", title="Popular MeSH Headings in 2020")
	bar_2021 = px.bar(trends_2021[:25],x="MeSH heading",y="Publication count", title="Popular MeSH Headings in 2021",color_discrete_sequence=["red"])
	bar_2022 = px.bar(trends_2022[:25],x="MeSH heading",y="Publication count", title="Popular MeSH Headings in 2022",color_discrete_sequence=["green"])
	bar_2023 = px.bar(trends_2023[:25],x="MeSH heading",y="Publication count", title="Popular MeSH Headings in 2023",color_discrete_sequence=["purple"])
	
	pub_fig=px.bar(pubs_df,
		x="researcher_id",
		y="score",color="preferred",
		color_discrete_sequence=px.colors.qualitative.Alphabet)

	pub_fig.update_layout(xaxis_title="Researcher", yaxis_title="Altmetric Score", showlegend=False,xaxis={'categoryorder':'total descending'})
	pub_fig.update_xaxes(tickvals=np.arange(15))

	app = Dash(__name__,external_stylesheets=[dbc.themes.LUX])

	content_style={
		"margin-left": "18rem",
		"margin-right": "18rem",
		"padding": "2rem 1rem"}

	app.layout = html.Div([
		html.H1('COVID-19 Data in Dimensions AI'),
		html.H2(children='Influential COVID researchers', style = {'textAlign':'Center','margin-left':'7px', 'margin-top':'7px'}),
			dcc.Graph(
			id='example-graph',
			figure=pub_fig, style={'margin-left':'7px', 'margin-top':'7px'}),

		html.H2(children='Top publications by Altmetric score', style = {'textAlign':'Center','margin-left':'7px', 'margin-top':'7px'}),

		dash_table.DataTable(style_data={
			'whiteSpace': 'normal',
			'height': 'auto',},data=top_5.to_dict('records'), page_size=5,style_table={'width':'75%'}),

		html.H2(children='Funding COVID-19 Research', style = {'textAlign':'Center'}),
		dash_table.DataTable(data=df_funds.to_dict('records'), page_size=25),

		html.H1(children='Leading COVID-19 Vaccine Research Institutions', style = {'textAlign':'Center'}),
		dcc.Graph(
			id='org_map',
			figure=scatter_fig, style={'margin-left':'2px', 'margin-top':'2px'}),
		html.H1(children='Leading COVID-19 Research Institutions', style = {'textAlign':'Center'}),

		dash_table.DataTable(style_data={
			'whiteSpace': 'normal',
			'height': 'auto'},
			data=df_all.to_dict('records'), page_size=25,style_table={'width':'75%'}),

		html.H1(children='Trends in COVID-19 Research', style = {'textAlign':'Center'}),
		dcc.Graph(
			id='sub1',
			figure=bar_2020, style={'margin-left':'7px', 'margin-top':'7px'}),
		dcc.Graph(
			id='sub2',
			figure=bar_2021, style={'margin-left':'7px', 'margin-top':'7px'}),
		dcc.Graph(
			id='sub3',
			figure=bar_2022, style={'margin-left':'7px', 'margin-top':'7px'}),
		dcc.Graph(
			id='sub4',
			figure=bar_2023, style={'margin-left':'7px', 'margin-top':'7px'}), 

		html.H1(children='Novel COVID-19 research', style = {'textAlign':'Center'}),
		dcc.Graph(
			id='keywords',
			figure=sun_fig, style={'margin-left':'2px', 'margin-top':'2px','width': '90vh', 'height': '90vh'})

	])

	app.run_server(debug=True)

if __name__ == '__main__':
	main()
