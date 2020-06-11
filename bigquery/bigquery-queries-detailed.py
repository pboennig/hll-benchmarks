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

#Housekeeping Data Structures
pct_diff_war_and_peace = []
hll_estimate_war_and_peace = []
time_war_and_peace = []

pct_diff_shakespeare = []
hll_estimate_shakespeare = []
time_shakespeare = []


pct_diff_ulysses = []
hll_estimate_ulysses = []
time_ulysses = []


EXACT_QUERY_TEMPLATE = 'SELECT COUNT(DISTINCT string_field_0) as exact_count  \
        FROM cs166.%s \
        WHERE RAND() < 2 '
APPROX_QUERY_TEMPLATE = 'SELECT HLL_COUNT.EXTRACT(HLL_COUNT.INIT(string_field_0, %d))\
            as approx_count FROM cs166.%s WHERE RAND() < 2  '


def calc_pct_diff(approx_count, exact_count):
    return round(((approx_count - exact_count) / exact_count) * 100, 2)

print('############################## WAR AND PEACE #################################')

# Exact Count.

start = time.perf_counter()
client = bigquery.Client()
QUERY = (EXACT_QUERY_TEMPLATE % 'war_and_peace')
query_job = client.query(QUERY)  # API request
rows = query_job.result()  # Waits for query to finish

for row in rows:
    print("exact count", row.get('exact_count'))
    exact_count = row.get('exact_count')

time_taken = time.perf_counter() - start
print("Time taken to compute exact count for War and Peace", time_taken)


# Approximate Count.

for precision in trange(10, 25):
    start = time.perf_counter()
    i = precision
    QUERY = (APPROX_QUERY_TEMPLATE % (i, 'war_and_peace'))
    client = bigquery.Client()
    query_job = client.query(QUERY)  # API request
    rows = query_job.result()  # Waits for query to finish

    for row in rows:        
        pct_diff = calc_pct_diff(row.get('approx_count'), exact_count)
        pct_diff_war_and_peace.append(pct_diff)        
        hll_estimate_war_and_peace.append(row.get('approx_count'))        
        if verbose:
            print("approx count with precision level, %d" % i, row.get('approx_count'))
            print("%% difference with precision level, %d" % i, pct_diff)        
        time_taken = time.perf_counter() - start
        time_war_and_peace.append(time_taken)
        
        if verbose:
            print("Time taken for this query", time_taken)
        
        
print('############################## SHAKESPEARE #################################')


# Exact Count.
start = time.perf_counter()
client = bigquery.Client()
QUERY = (EXACT_QUERY_TEMPLATE % 'shakespeare')        
query_job = client.query(QUERY)  # API request
rows = query_job.result()  # Waits for query to finish
for row in rows:
    print("exact count", row.get('exact_count'))
    exact_count = row.get('exact_count')

time_taken = time.perf_counter() - start
print("Time taken to compute exact count for Shakespeare", time_taken)

# Approximate Count.

for i in trange(10, 25):
    start = time.perf_counter()
    QUERY = (APPROX_QUERY_TEMPLATE % (i, 'shakespeare'))
    client = bigquery.Client() #for fair and consistent timing purposes
    query_job = client.query(QUERY)  # API request
    rows = query_job.result()  # Waits for query to finish
    for row in rows:        
        pct_diff = calc_pct_diff(row.get('approx_count'), exact_count)
        pct_diff_shakespeare.append(pct_diff)                
        hll_estimate_shakespeare.append(row.get('approx_count'))      
        if verbose:  
            print("approx count with precision level, %d" % i, row.get('approx_count'))
            print("%% difference with precision level, %d" % i, pct_diff)
        time_taken = time.perf_counter() - start
        time_shakespeare.append(time_taken)
        if verbose:
            print("Time taken for this query", time_taken)    

print('############################## ULYSSES #################################')

# Exact Count.
start = time.perf_counter()
QUERY = (EXACT_QUERY_TEMPLATE % 'ulysses')        
client = bigquery.Client()
query_job = client.query(QUERY)  # API request
rows = query_job.result()  # Waits for query to finish
for row in rows:
    print("exact count", row.get('exact_count'))
    exact_count = row.get('exact_count')
time_taken = time.perf_counter() - start
print("Time taken to compute exact count for Ulysses", time_taken)

# Approximate Count.

for i in trange(10, 25):
    start = time.perf_counter()
    QUERY = (APPROX_QUERY_TEMPLATE % (i, 'ulysses'))
    client = bigquery.Client() #repeating for timing purposes
    query_job = client.query(QUERY)  # API request
    rows = query_job.result()  # Waits for query to finish
    for row in rows:        
        pct_diff = calc_pct_diff(row.get('approx_count'), exact_count)
        pct_diff_ulysses.append(pct_diff)                
        hll_estimate_ulysses.append(row.get('approx_count'))
        if verbose:
            print("approx count with precision level, %d" % i, row.get('approx_count'))
            print("%% difference with precision level, %d" % i, pct_diff)
        time_taken = time.perf_counter() - start
        time_ulysses.append(time_taken)
        if verbose:
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
