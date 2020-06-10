import sys
import argparse
from python_hll.hll import HLL
import mmh3

parser = argparse.ArgumentParser(description='Estimate unique words in text file(s)')
parser.add_argument('file', metavar='F', type=str,  help="csv")
parser.add_argument('log2m', metavar='L', type=int)
parser.add_argument('reg_width', metavar='R', type=int)
a = parser.parse_args()

hll = HLL(a.log2m, a.reg_width)
with open(a.file, 'r') as f:
    for token in f:
        hashed_value = mmh3.hash(token)
        hll.add_raw(hashed_value)
print(hll.cardinality())
