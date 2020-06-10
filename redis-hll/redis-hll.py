import redis
import sys
import argparse
import nltk

parser = argparse.ArgumentParser(description='Estimate unique words in text file(s)')
parser.add_argument('files', metavar='F', type=str, nargs='+', help="list of files")
a = parser.parse_args()

r = redis.Redis()
r.flushdb() # new estimate each time

for file in a.files:
    f = open(file, "r")
    for token in f: 
        r.pfadd("hll", token)

estimate = r.pfcount("hll")
print(estimate) 
