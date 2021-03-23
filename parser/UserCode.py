from Errors import RestrictedCodeError
from Settings import safety_restricted_funcs
from Settings import other_restricted_funcs
from Settings import safety_restricted_keywords

import re


class UserCode:
    def __init__(self, filename):
        self.__code = self.__readAlgoFromFile(filename)

    @property
    def code(self):
        return self.__code
    
    @code.getter
    def code(self):
        return self.__code

    @staticmethod
    def __readAlgoFromFile(filename):
        algo = ""
        with open(filename, 'r') as f:
            for line in f.readlines():
                algo += line
        return algo
    
    def checkForRestricted(self):
        ''' returns True if code is free of restricted funcs. False otherwise '''
        restricted_funcs = safety_restricted_funcs + other_restricted_funcs

        for line in self.__code.split('\n'):
            for elem in restricted_funcs:
                if re.match(r'[^A-Za-z0-9_]*' + elem + r'\s*\([^A-Za-z0-9_]*', line):
                    # print("Usage of a restricted element", elem)
                    raise RestrictedCodeError("User code contains restricted function", elem)
                    # return False

            for elem in safety_restricted_keywords:
                if re.match(r'[^A-Za-z0-9_]*' + elem + r'[^A-Za-z0-9_]*', line):
                    # print("User cannot import any packages")
                    raise RestrictedCodeError("User code contains restricted keyword", elem)
                    # return False
        # return True

# cd = UserCode()
# cd.code = './parser/res/input/test_file.py'
# print(cd.checkForRestricted())
