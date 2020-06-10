import sys

uniq = set()
with open(sys.argv[1], "r") as f:
    for l in f: 
        tok = l.split()
        uniq.update(tok)

print(len(uniq))

for i in sorted(list(uniq)):
    print(i)