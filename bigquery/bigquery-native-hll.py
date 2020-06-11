from google.cloud import bigquery
from urllib.error import HTTPError
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/Surya/Surya/School/CS166/Project/key_files/surya-bigquery-project-editable-key.json"

client = bigquery.Client()

job_config = bigquery.LoadJobConfig()
job_config.source_format = bigquery.SourceFormat.CSV
job_config.skip_leading_rows = 1
job_config.autodetect = True
job_config._properties['load']['schemaUpdateOptions'] = ['ALLOW_FIELD_ADDITION']


############################## WAR AND PEACE #################################



############################## SHAKESPEARE #################################
table_id = "cs166-hll-279503.cs166.shakespeare"

schema = [
    bigquery.SchemaField("words", "STRING"),
    bigquery.SchemaField("string_field_0", "STRING")
]

table = bigquery.Table(table_id, schema=schema)


table = client.create_table(table)  # Make an API request.

print(
    "Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id)
)

filename = '/Users/Surya/Surya/School/CS166/Project/hll-benchmarks/text/shakespeare.csv'
dataset_id = 'cs166'
table_id = 'shakespeare'

dataset_ref = client.dataset(dataset_id)
table_ref = dataset_ref.table(table_id)

with open(filename, "rb") as source_file:
    job = client.load_table_from_file(source_file, table_ref, job_config=job_config)

job.result()  # Waits for table load to complete.

print("Loaded {} rows into {}:{}.".format(job.output_rows, dataset_id, table_id))


############################## ULYSSES #################################
table_id = "cs166-hll-279503.cs166.ulysses"

schema = [
    bigquery.SchemaField("words", "STRING"),
    bigquery.SchemaField("string_field_0", "STRING")
]

table = bigquery.Table(table_id, schema=schema)


table = client.create_table(table)  # Make an API request.

print(
    "Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id)
)

filename = '/Users/Surya/Surya/School/CS166/Project/hll-benchmarks/text/ulysses.csv'
dataset_id = 'cs166'
table_id = 'ulysses'

dataset_ref = client.dataset(dataset_id)
table_ref = dataset_ref.table(table_id)

with open(filename, "rb") as source_file:
    job = client.load_table_from_file(source_file, table_ref, job_config=job_config)

job.result()  # Waits for table load to complete.

print("Loaded {} rows into {}:{}.".format(job.output_rows, dataset_id, table_id))




