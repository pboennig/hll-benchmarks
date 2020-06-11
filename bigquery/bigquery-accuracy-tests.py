from google.cloud import bigquery
from urllib.error import HTTPError
import matplotlib.pyplot as plt
import os
import time
import tqdm 

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/Surya/Surya/School/CS166/Project/key_files/surya-bigquery-project-editable-key.json"

client = bigquery.Client()

################################# ACCURACY TESTS ###############################

QUERY = (
    'SELECT COUNT(DISTINCT string_field_0) as exact_count  \
        FROM cs166.ulysses')

start = time.process_time()
query_job = client.query(QUERY)  # API request
rows = query_job.result()  # Waits for query to finish
time_taken = time.process_time() - start
print("Time taken to compute exact count for Ulysses", time_taken)

for row in rows:
    print("exact count", row.get('exact_count'))
    exact_count = row.get('exact_count')

ulysses_accuracy = [[] for _ in range(10, 25)]

for precision in range(10, 25):
    i = precision

    QUERY = (
        'SELECT HLL_COUNT.EXTRACT(HLL_COUNT.INIT(string_field_0, %d))\
            as approx_count FROM cs166.ulysses' % i) 

    for j in tqdm.trange(10):    
        query_job = client.query(QUERY)  # API request
        rows = query_job.result()  # Waits for query to finish
                        
        for row in rows:
            pct_diff = round((((row.get('approx_count')) - exact_count) / exact_count) * 100, 2)
            ulysses_accuracy[i %len(ulysses_accuracy)].append(pct_diff)
            
    plt.plot(ulysses_accuracy[i%len(ulysses_accuracy)])

plt.xlabel('trial')
plt.xlabel('%% error')
plt.savefig('uly_acc.png')
