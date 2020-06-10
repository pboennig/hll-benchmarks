'''
Sweep over possible hyperparameters in Go
'''

import acc_test
import os
import matplotlib.pyplot as plt
import numpy as np

M_MIN = 4
M_MAX = 16

texts = ["../text/ulysses.csv", "../text/war_and_peace.csv", "../text/shakespeare.csv"]
encoding = "utf-8"
redis_path = os.path.join(os.path.dirname(__file__), "../redis-hll/redis-hll.py")
go_path = os.path.join(os.path.dirname(__file__), "../go-hll/go-hll.go")
py_path = os.path.join(os.path.dirname(__file__), "../python-hll/python-hll-simple.py")

gt, _ = acc_test.parse_files(texts)


def plot_results(res, texts):
    plt.title("Accuracy")
    plt.xlabel("b (address size)")
    plt.ylabel("absolute error (%)")
    for i in range(len(texts)):
        f = os.path.split(os.path.splitext(texts[i])[0])[-1]
        plt.scatter(np.arange(M_MIN, M_MAX+1), res[i,:,0], label=f)
    plt.legend(loc="upper right")
    plt.savefig("go_plots/acc.png")
    plt.clf()

    plt.title("Speed")
    plt.xlabel("b (address size)")
    plt.ylabel("time (s)")
    for i in range(len(texts)):
        f = os.path.split(os.path.splitext(texts[i])[0])[-1]
        plt.scatter(np.arange(M_MIN, M_MAX+1), res[i,:,1], label=f)
    plt.legend(loc="upper right")
    plt.savefig("go_plots/speed.png")
    plt.clf()

res = np.zeros((len(texts),M_MAX - M_MIN + 1, 2))
for i in range(len(texts)):
    f = list(gt.keys())[i]
    for m in range(M_MIN, M_MAX+1):
        command = ["go", "run", go_path, str(m), f]
        error, t = acc_test.acc_test(command,gt[f])
        res[i][m - M_MIN] = abs(error), t
plot_results(res, texts)
    


