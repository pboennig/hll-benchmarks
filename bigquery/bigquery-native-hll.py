from google.cloud import bigquery
from urllib.error import HTTPError
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/Surya/Surya/School/CS166/Project/key_files/surya-bigquery-project-editable-key.json"

client = bigquery.Client()

def doesTableExist(project_id, dataset_id, table_id):
    bq.tables().get(
        projectId=project_id, 
        datasetId=dataset_id,
        tableId=table_id).execute()
    return True

#  except HttpError err
#    if err.resp.status <> 404:
#       raise
#    return False

############################## WAR AND PEACE #################################

# Exact Count.
QUERY = (
    'SELECT COUNT(DISTINCT string_field_0) as exact_count  \
        FROM cs166.war_and_peace')
query_job = client.query(QUERY)  # API request
rows = query_job.result()  # Waits for query to finish

for row in rows:
    print("exact count", row.get('exact_count'))

# Approximate Count.

QUERY = (
    'SELECT HLL_COUNT.EXTRACT(HLL_COUNT.INIT(string_field_0)) as approx_count FROM cs166.war_and_peace')
query_job = client.query(QUERY)  # API request
rows = query_job.result()  # Waits for query to finish

for row in rows:
    print("approx count", row.get('approx_count'))


############################## SHAKESPEARE #################################
table_id = "cs166-hll-279503.cs166.shakespeare"

schema = [
    bigquery.SchemaField("words", "STRING"),
]

table = bigquery.Table(table_id, schema=schema)


#table = client.create_table(table)  # Make an API request.

#print(
#    "Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id)
#)



filename = '/path/to/file.csv'
dataset_id = 'my_dataset'
table_id = 'my_table'

dataset_ref = client.dataset(dataset_id)
table_ref = dataset_ref.table(table_id)
job_config = bigquery.LoadJobConfig()
job_config.source_format = bigquery.SourceFormat.CSV
job_config.skip_leading_rows = 1
job_config.autodetect = True

with open(filename, "rb") as source_file:
    job = client.load_table_from_file(source_file, table_ref, job_config=job_config)

job.result()  # Waits for table load to complete.

print("Loaded {} rows into {}:{}.".format(job.output_rows, dataset_id, table_id))



