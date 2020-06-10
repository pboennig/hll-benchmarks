'''
Returns number of unique tokens in file from argv[1]
'''
import sys
import csv

uniq = set()
with open(sys.argv[1], "r") as f:
    for row in f:
        uniq.add(row)

print(len(uniq))
