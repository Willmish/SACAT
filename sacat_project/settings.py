# import sys
# sys.setrecursionlimit(10**6)

DEBUG = False

fileFrom = "./res/temp/.sort.py"
fileTo = "./res/temp/.sort_edited.py"

safety_restricted_funcs = ["compile", "dir", "eval", "exec", "globals", 'input', 'open']
other_restricted_funcs = ["enumerate", "filter", 'iter', 'map', 'next', 'sorted', 'zip']
safety_restricted_keywords = ["import"]
