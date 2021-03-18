from Parser import Parser
from Analyzer import Analyzer
from Settings import *

if __name__ == '__main__':
    p = Parser()
    p.parseCode(fileFrom, fileTo)
    a = Analyzer()
    a.analyze((fileFrom, pathFrom, fileTo, pathTo))
    a.showAnalysisResults()
