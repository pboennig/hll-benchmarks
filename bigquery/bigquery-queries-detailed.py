from google.cloud import bigquery
from urllib.error import HTTPError
import os
import time

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/Surya/Surya/School/CS166/Project/key_files/surya-bigquery-project-editable-key.json"

client = bigquery.Client()

print('############################## WAR AND PEACE #################################')
# Exact Count.
QUERY = (
    'SELECT COUNT(DISTINCT string_field_0) as exact_count  \
        FROM cs166.war_and_peace')
query_job = client.query(QUERY)  # API request
rows = query_job.result()  # Waits for query to finish

for row in rows:
    print("exact count", row.get('exact_count'))
    exact_count = row.get('exact_count')

# Approximate Count.

for precision in range(10, 25):
    i = precision
    start = time.process_time()
    QUERY = (
        'SELECT HLL_COUNT.EXTRACT(HLL_COUNT.INIT(string_field_0, %d))\
            as approx_count FROM cs166.war_and_peace' % i) 
    time_taken = time.process_time() - start

    query_job = client.query(QUERY)  # API request
    rows = query_job.result()  # Waits for query to finish

    for row in rows:
        print("approx count with precision level, %d" % i, row.get('approx_count'))
        pct_diff = round((((row.get('approx_count')) - exact_count) / exact_count) * 100, 2)
        print("%% difference with precision level, %d" % i, pct_diff)
        print("Time taken for this query", time_taken)
        

print('############################## SHAKESPEARE #################################')

# Exact Count.
QUERY = (
    'SELECT COUNT(DISTINCT string_field_0) as exact_count  \
        FROM cs166.shakespeare')
query_job = client.query(QUERY)  # API request
rows = query_job.result()  # Waits for query to finish

for row in rows:
    print("exact count", row.get('exact_count'))

# Approximate Count.

QUERY = (
    'SELECT HLL_COUNT.EXTRACT(HLL_COUNT.INIT(string_field_0))\
         as approx_count FROM cs166.shakespeare')
query_job = client.query(QUERY)  # API request
rows = query_job.result()  # Waits for query to finish

for row in rows:
    print("approx count", row.get('approx_count'))

print('############################## ULYSSES #################################')

# Exact Count.
QUERY = (
    'SELECT COUNT(DISTINCT string_field_0) as exact_count  \
        FROM cs166.ulysses')
query_job = client.query(QUERY)  # API request
rows = query_job.result()  # Waits for query to finish

for row in rows:
    print("exact count", row.get('exact_count'))

# Approximate Count.

QUERY = (
    'SELECT HLL_COUNT.EXTRACT(HLL_COUNT.INIT(string_field_0))\
         as approx_count FROM cs166.ulysses')
query_job = client.query(QUERY)  # API request
rows = query_job.result()  # Waits for query to finish

for row in rows:
    print("approx count", row.get('approx_count'))