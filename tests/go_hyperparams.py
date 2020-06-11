'''
Sweep over possible hyperparameters in Go
'''

import os
import matplotlib.pyplot as plt
import numpy as np
import time
import subprocess
import acc_test

# hyperparameters for Go
M_MIN = 4
M_MAX = 16
num_trials = 5

texts = ["../text/ulysses.csv", "../text/war_and_peace.csv", "../text/shakespeare.csv"]
encoding = "utf-8"
redis_path = os.path.join(os.path.dirname(__file__), "../redis-hll/redis-hll.py")
go_path = os.path.join(os.path.dirname(__file__), "../go-hll/go-hll.go")
py_path = os.path.join(os.path.dirname(__file__), "../python-hll/python-hll-simple.py")

gt, _ = acc_test.parse_files(texts)

res = np.zeros((num_trials, len(texts),M_MAX - M_MIN + 1, 2))

for n in range(num_trials):
    for i in range(len(texts)):
        f = list(gt.keys())[i]
        for m in range(M_MIN, M_MAX+1):
            command = ["go", "run", go_path, str(m), f]
            res[n][i][m - M_MIN] = acc_test.estimate(command)

res = res.mean(axis=0)
np.save("go_plots/go_plots.npy", res)


