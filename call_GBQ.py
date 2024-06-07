from google.cloud import bigquery
import numpy as np

def run_query(q):

    client = bigquery.Client.from_service_account_json("../key.json") #specify path to GBQ service account key
    query_job = client.query(q)
    print("This query will process {} bytes.".format(query_job.total_bytes_processed))
    query_result = query_job.result()
    df = query_result.to_dataframe()
    return df

#query to retrieve top 100 research organizations in COVID vaccine research
res_query = ('SELECT `covid-19-dimensions-ai.data.grid`.name AS Institution, `covid-19-dimensions-ai.data.grid`.address.country as Country,`covid-19-dimensions-ai.data.grid`.address.city as City, TO_JSON_STRING(`covid-19-dimensions-ai.data.grid`.types) AS t, count(r) as c '
    'FROM (SELECT research_orgs FROM '
    '`covid-19-dimensions-ai.data.publications` '
    'WHERE ("COVID-19 Vaccines" IN UNNEST(mesh_headings))), UNNEST(research_orgs) as r '
    'LEFT JOIN  `covid-19-dimensions-ai.data.grid` ON '
    '`covid-19-dimensions-ai.data.grid`.id= r '
    'GROUP BY Institution,Country,City,t '
    'ORDER BY c DESC '
    'LIMIT 100')
#query to retrieve top 100 research organizations in all COVID research
all_query = ('SELECT `covid-19-dimensions-ai.data.grid`.name AS Institution, `covid-19-dimensions-ai.data.grid`.address.country as Country,`covid-19-dimensions-ai.data.grid`.address.city as City, TO_JSON_STRING(`covid-19-dimensions-ai.data.grid`.types) AS t, count(r) as c '
    'FROM (SELECT research_orgs FROM '
    '`covid-19-dimensions-ai.data.publications`), UNNEST(research_orgs) as r '
    'LEFT JOIN  `covid-19-dimensions-ai.data.grid` ON '
    '`covid-19-dimensions-ai.data.grid`.id= r '
    'GROUP BY Institution,Country,City,t '
    'ORDER BY c DESC '
    'LIMIT 100')

#query to retrieve top 1000 publications
pub_QUERY = ('SELECT altmetrics.score,title.preferred,a.last_name,a.first_name,a.researcher_id FROM `covid-19-dimensions-ai.data.publications`, '
    'UNNEST(authors) AS a '
    'ORDER BY altmetrics.score DESC '
    'LIMIT 10000')

#query to retrieve top funders

fund_query = ('SELECT `covid-19-dimensions-ai.data.grid`.name, '
  '`covid-19-dimensions-ai.data.grants`.funder_org, '
  'SUM(`covid-19-dimensions-ai.data.grants`.funding_usd) AS amt '
  'FROM `covid-19-dimensions-ai.data.grants` '
  'LEFT JOIN `covid-19-dimensions-ai.data.grid` '
  'ON `covid-19-dimensions-ai.data.grid`.id= `covid-19-dimensions-ai.data.grants`.funder_org '
  'GROUP BY `covid-19-dimensions-ai.data.grid`.name,`covid-19-dimensions-ai.data.grants`.funder_org '
  'ORDER BY amt DESC')

#query to retrieve top MeSH headings by year
trend_q = ('SELECT year,h,COUNT(h) as h_c FROM `covid-19-dimensions-ai.data.publications`, UNNEST(mesh_headings) AS h '
    'GROUP BY h,year '
    'ORDER by year,h_c DESC ')

df_res = run_query(res_query)
df_all = run_query(all_query)  
df_funds = run_query(fund_query)
df_pubs= run_query(pub_QUERY)
years_df = run_query(trend_q)
  