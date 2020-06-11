from google.cloud import bigquery
from urllib.error import HTTPError
import matplotlib.pyplot as plt
import os
import time


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/Surya/Surya/School/CS166/Project/key_files/surya-bigquery-project-editable-key.json"

client = bigquery.Client()

print('############################## WAR AND PEACE #################################')
# Exact Count.

pct_diff_war_and_peace = []

time_war_and_peace = []

QUERY = (
    'SELECT COUNT(DISTINCT string_field_0) as exact_count  \
        FROM cs166.war_and_peace')

start = time.process_time()
query_job = client.query(QUERY)  # API request
rows = query_job.result()  # Waits for query to finish
time_taken = time.process_time() - start
print("Time taken to compute exact count for War and Peace", time_taken)

for row in rows:
    print("exact count", row.get('exact_count'))
    exact_count = row.get('exact_count')

# Approximate Count.

for precision in range(10, 25):
    i = precision

    QUERY = (
        'SELECT HLL_COUNT.EXTRACT(HLL_COUNT.INIT(string_field_0, %d))\
            as approx_count FROM cs166.war_and_peace' % i) 
    
    start = time.process_time()
    query_job = client.query(QUERY)  # API request
    rows = query_job.result()  # Waits for query to finish
    time_taken = time.process_time() - start

    for row in rows:
        print("approx count with precision level, %d" % i, row.get('approx_count'))
        pct_diff = round((((row.get('approx_count')) - exact_count) / exact_count) * 100, 2)
        pct_diff_war_and_peace.append(pct_diff)
        print("%% difference with precision level, %d" % i, pct_diff)
        print("Time taken for this query", time_taken)
        time_war_and_peace.append(time_taken)
        

print('############################## SHAKESPEARE #################################')

pct_diff_shakespeare = []

time_shakespeare = []

# Exact Count.
QUERY = (
    'SELECT COUNT(DISTINCT string_field_0) as exact_count  \
        FROM cs166.shakespeare')
start = time.process_time()
query_job = client.query(QUERY)  # API request
rows = query_job.result()  # Waits for query to finish
time_taken = time.process_time() - start
print("Time taken to compute exact count for Shakespeare", time_taken)

for row in rows:
    print("exact count", row.get('exact_count'))
    exact_count = row.get('exact_count')

# Approximate Count.

for precision in range(10, 25):
    i = precision
    
    QUERY = (
        'SELECT HLL_COUNT.EXTRACT(HLL_COUNT.INIT(string_field_0, %d))\
            as approx_count FROM cs166.shakespeare' % i) 
    
    start = time.process_time()
    query_job = client.query(QUERY)  # API request
    rows = query_job.result()  # Waits for query to finish
    time_taken = time.process_time() - start

    for row in rows:
        print("approx count with precision level, %d" % i, row.get('approx_count'))
        pct_diff = round(((row.get('approx_count') - exact_count) / exact_count) * 100, 2)
        pct_diff_shakespeare.append(pct_diff)
        print("%% difference with precision level, %d" % i, pct_diff)
        print("Time taken for this query", time_taken)    
        time_shakespeare.append(time_taken)

print('############################## ULYSSES #################################')

pct_diff_ulysses = []
time_ulysses = []

# Exact Count.
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

# Approximate Count.

for precision in range(10, 25):
    i = precision

    QUERY = (
        'SELECT HLL_COUNT.EXTRACT(HLL_COUNT.INIT(string_field_0, %d))\
            as approx_count FROM cs166.ulysses' % i) 

    start = time.process_time()
    query_job = client.query(QUERY)  # API request
    rows = query_job.result()  # Waits for query to finish
    time_taken = time.process_time() - start

    for row in rows:
        print("approx count with precision level, %d" % i, row.get('approx_count'))
        pct_diff = round((((row.get('approx_count')) - exact_count) / exact_count) * 100, 2)
        pct_diff_ulysses.append(pct_diff)
        print("%% difference with precision level, %d" % i, pct_diff)
        print("Time taken for this query", time_taken)    
        time_ulysses.append(time_taken)


################################# PLOTTING ###############################


# plt.scatter(x = range(10, 25),  y = pct_diff_shakespeare, label = 'Shakespeare')
# plt.scatter(x = range(10, 25),  y = pct_diff_ulysses, label = 'Ulysses')
# plt.scatter(x = range(10, 25),  y = pct_diff_war_and_peace, label = 'War and Peace')
# plt.xlabel('Level of Precision (higher is better)')
# plt.ylabel('% error')
# plt.legend()
# plt.savefig('one-run-accuracy vs precision hyperparam.png')




plt.scatter(x = range(10, 25),  y = time_shakespeare, label = 'Shakespeare')
plt.scatter(x = range(10, 25),  y = time_ulysses, label = 'Ulysses')
plt.scatter(x = range(10, 25),  y = time_war_and_peace, label = 'War and Peace')
plt.xlabel('Level of Precision (higher is better)')
plt.ylabel('Time taken Per Query (higher is better)')
plt.legend()
plt.savefig('bigquery-timing.png')


