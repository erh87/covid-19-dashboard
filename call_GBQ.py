from google.cloud import bigquery
import numpy as np

def run_query(q):

    client = bigquery.Client.from_service_account_json("key.json")
    query_job = client.query(q)
    print("This query will process {} bytes.".format(query_job.total_bytes_processed))
    query_result = query_job.result()
    df = query_result.to_dataframe()
    return df