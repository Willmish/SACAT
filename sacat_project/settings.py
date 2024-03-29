# import sys
# sys.setrecursionlimit(10**6)

DEBUG = False

fileFrom = "./res/input/.sort.py"
fileTo = "./res/input/.sort_edited.py"

safety_restricted_funcs = ["compile", "dir", "eval", "exec", "globals", 'input', 'open']
other_restricted_funcs = ["enumerate", "filter", 'iter', 'map', 'next', 'sorted', 'zip']
safety_restricted_keywords = ["import"]
