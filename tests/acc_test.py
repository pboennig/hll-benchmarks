import shlex, subprocess
import os
import time

texts = ["../text/ulysses.txt", "../text/war_and_peace.txt"]
encoding = "utf-8"
script_path = os.path.join(os.path.dirname(__file__), "../redis-hll/redis-hll.py")
go_path = os.path.join(os.path.dirname(__file__), "../go-hll/go-hll.go")

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

def test_redis(gt, lengths):
    print("Testing Redis....")
    print("{}".format('='*20))
    redis = subprocess.Popen("redis-server", stdout=subprocess.PIPE)
    for txt_path, card in gt.items(): 
        print("Testing file {} with {} tokens ({} unique)".format(txt_path, lengths[txt_path], card))
        t0 = time.time()
        estimator = subprocess.Popen(["python3", script_path, txt_path], stdout=subprocess.PIPE)
        guess = estimator.communicate()[0].decode(encoding).rstrip()
        t1 = time.time()
        print("Error: {:.2%}".format(int(guess) / card - 1))
        print("Took {:.2f} seconds".format(t1-t0))
    redis.kill()
    print("")

def test_go(gt, lengths) :
    print("Testing Go...")
    print("{}".format('='*20))
    for m in range(6, 14, 2):
        print("With {} buckets:".format(m))
        for txt_path, card in gt.items(): 
            print("Testing file {} with {} tokens ({} unique)".format(txt_path, lengths[txt_path], card))
            t0 = time.time()
            estimator = subprocess.Popen(["go", "run", go_path, str(m), txt_path], stdout=subprocess.PIPE)
            guess = estimator.communicate()[0].decode(encoding).rstrip()
            t1 = time.time()
            print("Error: {:.2%}".format(int(guess) / card - 1))
            print("Took {:.2f} seconds".format(t1-t0))
        print("")


if __name__=="__main__":
    gt, lengths = parse_files(texts)
    test_redis(gt, lengths)
    test_go(gt, lengths)
