from Parser import Parser

fileFrom = "parser/res/input/test_file.py"
fileTo = "parser/res/output/test_file_edited.py"


if __name__ == '__main__':
    p = Parser()
    p.parseCode(fileFrom, fileTo)