from google.cloud import bigquery
from urllib.error import HTTPError
import numpy as np
import matplotlib.pyplot as plt
import os
import time
import pickle
from tqdm import trange
verbose = False
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/Surya/Surya/School/CS166/Project/key_files/surya-bigquery-project-editable-key.json"

client = bigquery.Client()

print('############################## WAR AND PEACE #################################')
# Exact Count.

pct_diff_war_and_peace = []
hll_estimate_war_and_peace = []
time_war_and_peace = []

QUERY = (
    'SELECT COUNT(DISTINCT string_field_0) as exact_count  \
        FROM cs166.war_and_peace \
        WHERE RAND() < 2  ')

start = time.perf_counter()
query_job = client.query(QUERY)  # API request
rows = query_job.result()  # Waits for query to finish
time_taken = time.perf_counter() - start
print("Time taken to compute exact count for War and Peace", time_taken)

for row in rows:
    print("exact count", row.get('exact_count'))
    exact_count = row.get('exact_count')

# Approximate Count.

for precision in trange(10, 25):
    i = precision

    QUERY = (
        'SELECT HLL_COUNT.EXTRACT(HLL_COUNT.INIT(string_field_0, %d))\
            as approx_count FROM cs166.war_and_peace WHERE RAND() < 2  ' % i) 
    
    start = time.perf_counter()
    query_job = client.query(QUERY)  # API request
    rows = query_job.result()  # Waits for query to finish
    time_taken = time.perf_counter() - start

    for row in rows:
        
        pct_diff = round((((row.get('approx_count')) - exact_count) / exact_count) * 100, 2)
        pct_diff_war_and_peace.append(pct_diff)
        time_war_and_peace.append(time_taken)
        hll_estimate_war_and_peace.append(row.get('approx_count'))
        if verbose:
            print("approx count with precision level, %d" % i, row.get('approx_count'))
            print("%% difference with precision level, %d" % i, pct_diff)
            print("Time taken for this query", time_taken)
        
        

print('############################## SHAKESPEARE #################################')

pct_diff_shakespeare = []
hll_estimate_shakespeare = []
time_shakespeare = []

# Exact Count.
QUERY = (
    'SELECT COUNT(DISTINCT string_field_0) as exact_count  \
        FROM cs166.shakespeare WHERE RAND() < 2  ')
start = time.perf_counter()
query_job = client.query(QUERY)  # API request
rows = query_job.result()  # Waits for query to finish
time_taken = time.perf_counter() - start
print("Time taken to compute exact count for Shakespeare", time_taken)

for row in rows:
    print("exact count", row.get('exact_count'))
    exact_count = row.get('exact_count')

# Approximate Count.

for precision in trange(10, 25):
    i = precision
    
    QUERY = (
        'SELECT HLL_COUNT.EXTRACT(HLL_COUNT.INIT(string_field_0, %d))\
            as approx_count FROM cs166.shakespeare WHERE RAND() < 2  ' % i) 
    
    start = time.perf_counter()
    query_job = client.query(QUERY)  # API request
    rows = query_job.result()  # Waits for query to finish
    time_taken = time.perf_counter() - start

    for row in rows:
        
        pct_diff = round(((row.get('approx_count') - exact_count) / exact_count) * 100, 2)
        pct_diff_shakespeare.append(pct_diff)        
        time_shakespeare.append(time_taken)
        hll_estimate_shakespeare.append(row.get('approx_count'))      
        if verbose:  
            print("approx count with precision level, %d" % i, row.get('approx_count'))
            print("%% difference with precision level, %d" % i, pct_diff)
            print("Time taken for this query", time_taken)    

print('############################## ULYSSES #################################')

pct_diff_ulysses = []
hll_estimate_ulysses = []
time_ulysses = []

# Exact Count.
QUERY = (
    'SELECT COUNT(DISTINCT string_field_0) as exact_count  \
        FROM cs166.ulysses WHERE RAND() < 2  ')

start = time.perf_counter()
query_job = client.query(QUERY)  # API request
rows = query_job.result()  # Waits for query to finish
time_taken = time.perf_counter() - start
print("Time taken to compute exact count for Ulysses", time_taken)

for row in rows:
    print("exact count", row.get('exact_count'))
    exact_count = row.get('exact_count')

# Approximate Count.

for precision in trange(10, 25):
    i = precision

    QUERY = (
        'SELECT HLL_COUNT.EXTRACT(HLL_COUNT.INIT(string_field_0, %d))\
            as approx_count FROM cs166.ulysses WHERE RAND() < 2  ' % i) 

    start = time.perf_counter()
    query_job = client.query(QUERY)  # API request
    rows = query_job.result()  # Waits for query to finish
    time_taken = time.perf_counter() - start

    for row in rows:        
        pct_diff = round((((row.get('approx_count')) - exact_count) / exact_count) * 100, 2)
        pct_diff_ulysses.append(pct_diff)        
        time_ulysses.append(time_taken)
        hll_estimate_ulysses.append(row.get('approx_count'))
        if verbose:
            print("approx count with precision level, %d" % i, row.get('approx_count'))
            print("%% difference with precision level, %d" % i, pct_diff)
            print("Time taken for this query", time_taken)    

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
plt.ylabel('Time taken Per Query')
plt.legend()
plt.savefig('bigquery-timing.png')

################################# PICKLING ###############################

hll_estimates = np.array([hll_estimate_shakespeare, hll_estimate_ulysses, hll_estimate_war_and_peace])

pickle_out = open("hll_estimates(Shakespeare, Ulysses, WandP).pickle","wb")
pickle.dump(hll_estimates, pickle_out)
pickle_out.close()

hll_times = np.array([time_shakespeare, time_ulysses, time_war_and_peace])

pickle_out = open("hll_times(Shakespeare, Ulysses, WandP).pickle","wb")
pickle.dump(hll_times, pickle_out)
pickle_out.close()

pickle_out = open("Precision_in_Range.pickle","wb")
pickle.dump(list(range(10, 25)), pickle_out)
pickle_out.close()
