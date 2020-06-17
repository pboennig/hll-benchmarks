from google.cloud import bigquery
import os
import sys
import argparse

parser = argparse.ArgumentParser(description='Estimate unique words in text file(s)')
parser.add_argument('precision', metavar='p', type=int, help="list of files")
parser.add_argument('file', metavar='F', type=str)
a = parser.parse_args()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "../../surya-bigquery-project-editable-key.json"

client = bigquery.Client()

texts = {"ulysses.csv" : "cs166.ulysses", 
         "war_and_peace.csv" : "cs166.war_and_peace",
         "shakespeare.csv" : "cs166.shakespeare"}
filename = os.path.split(a.file)[-1]
text = texts[filename]
QUERY = 'SELECT HLL_COUNT.EXTRACT(HLL_COUNT.INIT(string_field_0, {})) as approx_count FROM {}'.format(a.precision, text) 
query_job = client.query(QUERY)
rows = query_job.result()  # Waits for query to finish
for row in rows:
    print(row.get('approx_count'))
