from Parser import Parser

fileFrom = "parser/experiments/codeExamples/test_file.py"
fileTo = "parser/experiments/codeExamplesEdited/test_file_edited.py"


p = Parser()
p.parseCode(fileFrom, fileTo)