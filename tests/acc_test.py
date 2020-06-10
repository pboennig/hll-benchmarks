import shlex, subprocess
import os
import time

texts = ["../text/ulysses.csv", "../text/war_and_peace.csv"]
encoding = "utf-8"
redis_path = os.path.join(os.path.dirname(__file__), "../redis-hll/redis-hll.py")
go_path = os.path.join(os.path.dirname(__file__), "../go-hll/go-hll.go")
py_path = os.path.join(os.path.dirname(__file__), "../python-hll/python-hll-simple.py")

'''
For a given list of text paths, counts the number of total and unique tokens in the file.
Returns two dicts, ground_truth holds the cardinalities and lengths holds the total token counts, both
keyed by the paths.
'''
def parse_files(texts):
    ground_truth = {}
    lengths = {}
    for text in texts:
        path = os.path.join(os.path.dirname(__file__), text)
        uniq = set()
        length = 0
        with open(path, "r") as f:
            for l in f: 
                uniq.add(l)
                length += 1 

        ground_truth[path] = len(uniq)
        lengths[path] = length
    return ground_truth, lengths

'''
Estimates cardinality. Command must print out its cardinality guess, which is captured and converted
into an int. Also times subprocess.
'''
def estimate(command):
    t0 = time.time()
    estimator = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    guess = estimator.communicate()[0].decode(encoding).rstrip()
    t1 = time.time()
    t = t1-t0
    return int(guess), t

'''
Compares estimate to the ground truth cardinality.
'''
def acc_test(command, card):
    guess, t = estimate(command)
    error = guess / card - 1
    return error, t

'''
Pretty print of results of accuracy test error/time results for a given program prog (e.g. Go, Python, etc.)
'''
def print_acc_test(prog, error, t):
    print("{}:\t".format(prog) + "Error: {:.2%}".format(error) + "\t" + "Time: {:.2f} seconds".format(t))

'''
Runs acc_test for Redis, spinning up and killing redis-server as necessary.
'''
def test_redis(txt_path, gt):
    redis = subprocess.Popen("redis-server", stdout=subprocess.PIPE)
    command = ["python3", redis_path, txt_path]
    error, t = acc_test(command, gt[txt_path])
    print_acc_test("Redis", error, t)
    redis.kill()

'''
Runs acc_test for Go
'''
def test_go(txt_path, gt):
    command = ["go", "run", go_path, str(10), txt_path]
    error, t = acc_test(command, gt[txt_path])
    print_acc_test("Go", error, t)

'''
Runs acc_test for Python.
'''
def test_py(txt_path, gt):
    command = ["python3", py_path, txt_path, str(13), str(5)] 
    error, t = acc_test(command, gt[txt_path])
    print_acc_test("Python", error, t)

if __name__=="__main__":
    gt, lengths = parse_files(texts)
    for text in gt.keys():
        print("Testing file {} with {} tokens ({} unique)".format(text, lengths[text], gt[text]))
        print("-"*20)
        test_redis(text, gt)
        test_go(text, gt)
        test_py(text, gt)
        print("")
