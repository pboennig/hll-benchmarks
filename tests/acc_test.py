import shlex, subprocess
import os
import time

texts = ["../text/ulysses.txt", "../text/war_and_peace.txt"]
encoding = "utf-8"
script_path = os.path.join(os.path.dirname(__file__), "../redis-hll/redis-hll.py")
go_path = os.path.join(os.path.dirname(__file__), "../go-hll/go-hll.go")

'''
For a given list of text paths, counts the number of total and unique tokens in the file.
Returns two dicts, ground_truth holds the cardinalities and lengths holds the total token counts.
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
                tok = l.split()
                uniq.update(tok)
                length += len(tok)
        ground_truth[path] = len(uniq)
        lengths[path] = length
    return ground_truth, lengths

'''
Runs accuracy test for a given command by spinning up a subprocess, capturing the output,
and comparing it to the ground truth cardinality.
'''
def acc_test(command, txt_path, lengths, card):
    file_name = os.path.split(txt_path)[-1]
    print("Testing file {} with {} tokens ({} unique)".format(file_name, lengths[txt_path], card))
    print("-"*20)
    t0 = time.time()
    estimator = subprocess.Popen(command, stdout=subprocess.PIPE)
    guess = estimator.communicate()[0].decode(encoding).rstrip()
    t1 = time.time()
    print("Error: {:.2%}".format(int(guess) / card - 1))
    print("Took {:.2f} seconds".format(t1-t0))
    print("")

'''
Runs acc_test for Redis, spinning up and killing redis-server as necessary.
'''
def test_redis(gt, lengths):
    print("Testing Redis....")
    print("{}".format('='*20))
    redis = subprocess.Popen("redis-server", stdout=subprocess.PIPE)
    for txt_path, card in gt.items(): 
        command = ["python3", script_path, txt_path]
        acc_test(command, txt_path, lengths, card)

    redis.kill()
    print("")

'''
Runs acc_test for Go, iterating over possible bucket sizes to test
hyperparamter response.
'''
def test_go(gt, lengths) :
    print("Testing Go...")
    print("{}".format('='*20))
    for m in range(6, 14, 2):
        print("With {} buckets:".format(m))
        for txt_path, card in gt.items(): 
            command = ["go", "run", go_path, str(m), txt_path]
            acc_test(command, txt_path, lengths, card)
        print("")

if __name__=="__main__":
    gt, lengths = parse_files(texts)
    test_redis(gt, lengths)
    test_go(gt, lengths)
