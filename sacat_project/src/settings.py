import sys
sys.setrecursionlimit(10**6)

DEBUG = False
# DEBUG = True

# fileFrom = "./../../res/input/test_file.py"
# fileTo = "./../../res/output/test_file_edited.py"

fileFrom = "./../res/input/merge_sort.py"
fileTo = "./../res/output/merge_sort_edited.py"

# fileFrom = "./../res/input/quick_sort.py"
# fileTo = "./../res/output/quick_sort_edited.py"

# Restricted functions/keywords

safety_restricted_funcs = ["compile", "dir", "eval", "exec", "globals", 'input', 'open']
other_restricted_funcs = ["enumerate", "filter", 'iter', 'map', 'next', 'sorted', 'zip']
safety_restricted_keywords = ["import"]
