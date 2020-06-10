from google.cloud import bigquery
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/Surya/Surya/School/cs166/Project/Presto-HLL/surya-bigquery-project-editable-key.json"

client = bigquery.Client()

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

