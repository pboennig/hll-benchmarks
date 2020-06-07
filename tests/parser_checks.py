import shlex, subprocess
import os
import time

go_parse = "go_parse.go"
py_parse = "py_parse.py"
texts = ["../text/ulysses.txt", "../text/war_and_peace.txt", "../text/shakespeare.txt"]
encoding = "utf-8"

for text in texts:
    file_name = os.path.split(text)[-1]
    print("File: {}".format(file_name))
    print("="*20)
    txt_path = os.path.join(os.path.dirname(__file__), text)
    py_uniq = subprocess.Popen(["python3", py_parse, txt_path], stdout=subprocess.PIPE)
    py_card = int(py_uniq.communicate()[0].decode(encoding).rstrip())
    go_uniq = subprocess.Popen(["go", "run", go_parse, txt_path], stdout=subprocess.PIPE)
    go_card = int(go_uniq.communicate()[0].decode(encoding).rstrip())
    print("Python unique tokens: {}".format(py_card))
    print("Go unique tokens: {}".format(go_card))
    if py_card == go_card:
        print("PASS")
    else:
        print("FAIL")
    print("")
