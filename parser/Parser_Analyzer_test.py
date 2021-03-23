from Parser import Parser
from Analyzer import Analyzer
from Settings import *
from UserCode import UserCode

if __name__ == '__main__':
    # load user code and create User Code obj
    uc = UserCode(fileFrom)
    # check if the code contains restricted stuff
    uc.checkForRestricted()

    # create Parser obj
    p = Parser()
    # parse code and store it in fileTo
    p.parseCode(uc, fileTo)

    # create Analyzer obj
    a = Analyzer()
    # analyze code (instead of reading files analyzer imports them)
    a.generate_operations_table(fileFrom)
    print(a.operations_table)
    a.initModules(fileFrom, fileTo)
    a.executeAlgorithm()
    a.analyze()
    a.showAnalysisResults()
    # tmp func just for showing results in terminal
    # a.test_analyze((fileFrom, fileTo))
    # a.showAnalysisResults()
