from google.cloud import bigquery
from urllib.error import HTTPError
import numpy as np
import matplotlib.pyplot as plt
import os
import time
import pickle
from tqdm import trange
verbose = False
kMinPrecision = 10
kMaxPrecision = 25
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

def query_exact_count(database_name):
    start = time.perf_counter()
    client = bigquery.Client()
    QUERY = (EXACT_QUERY_TEMPLATE % database_name)
    query_job = client.query(QUERY)  # API request
    rows = query_job.result()  # Waits for query to finish
    for row in rows:        
        exact_count = row.get('exact_count')
    time_taken = time.perf_counter() - start
    if verbose:
        print("Time taken to compute exact count for %s" % database_name, time_taken)
        print("exact count", exact_count)

def query_approximate_count(database_name, estimate_arr, times_arr):
    for i in trange(kMinPrecision, kMaxPrecision):
        start = time.perf_counter()
        QUERY = (APPROX_QUERY_TEMPLATE % (i, database_name))
        client = bigquery.Client() #for timing purposes
        query_job = client.query(QUERY)  # API request
        rows = query_job.result()  # Waits for query to finish
        for row in rows:        
            approx_count = row.get('approx_count')
            estimate_arr.append(approx_count)        
            if verbose:
                print("approx count with precision level, %d" % i, approx_count)      
            time_taken = time.perf_counter() - start
            times_arr.append(time_taken)            
            if verbose:
                print("Time taken for this query", time_taken)
    

print(10 * '=' + 'WAR AND PEACE' + 10 * '=')
# Exact Count.
query_exact_count('war_and_peace')
# Approximate Count.
query_approximate_count('war_and_peace', hll_estimate_war_and_peace, time_war_and_peace)      
        
print(10 * '=' + 'SHAKESPEARE' + 10 * '=')
# Exact Count.
query_exact_count('shakespeare')
# Approximate Count.
query_approximate_count('shakespeare', hll_estimate_shakespeare, time_shakespeare)      

print(10 * '=' + 'ULYSSES' + 10 * '=')
# Exact Count.
query_exact_count('ulysses')
# Approximate Count.
query_approximate_count('ulysses', hll_estimate_ulysses, time_ulysses)      

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
