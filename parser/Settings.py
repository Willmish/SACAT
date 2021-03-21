DEBUG = True

fileFrom = "./parser/res/input/test_file.py"
fileTo = "./parser/res/output/test_file_edited.py"
pathFrom = "./parser/res/input/test_file.py"
pathTo = "./parser/res/output/test_file_edited.py"

# Restricted functions/keywords

safety_restricted_funcs = ["compile", "dir", "eval", "exec", "globals", 'input', 'print', 'open']
other_restricted_funcs = ["enumerate", "filter", 'iter', 'map', 'next', 'sorted', 'zip']
safety_restricted_keywords = ["import"]