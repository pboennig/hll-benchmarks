import redis
import sys
import argparse

parser = argparse.ArgumentParser(description='Estimate unique words in text file(s)')
parser.add_argument('files', metavar='F', type=str, nargs='+', help="list of files")
a = parser.parse_args()

r = redis.Redis()
r.flushdb() # new estimate each time

for file in a.files:
    f = open(file, "r")
    for l in f:
        words = l.split()
        for word in words:
            r.pfadd("hll", word) 

estimate = r.pfcount("hll")
print(estimate) 
