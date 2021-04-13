"""
Operation complexity analysis module.

Written by Andrzej Szablewski, March 2021.
"""

from src.runenv.test_super import SortTest


class OpAnalyzer(SortTest):
    def __init__(self, parsedModule, operations_table, test_name):
        self.__operations_table = operations_table  # Key - line number. Value - list of op codes
        self.__lines_execution = {}  # Key - line number. Value - number of executions
        self.__operation_count = {}  # Key - op code. Value - number of executions
        self.__test_name = test_name

        self.__parsedModule = parsedModule

    def countStackOperations(self):
        self.__operation_count = {}
        for key in self.__operations_table:
            for opcode in self.__operations_table[key]:
                if opcode not in self.__operation_count:
                    self.__operation_count[opcode] = self.__lines_execution[key]
                else:
                    self.__operation_count[opcode] += self.__lines_execution[key]

    def executeAlgorithm(self, array):
        sorted_arr = None
        try:
            sorted_arr = self.__parsedModule.mySort(array)
            self.__lines_execution = self.__parsedModule.lines_dict.copy()
            self.clearLinesDict()
        except Exception as e:
            print("User algorithm error.", str(e))
        return sorted_arr

    def clearLinesDict(self):
        for k in self.__parsedModule.lines_dict.keys():
            self.__parsedModule.lines_dict[k] = 0

    def analyse(self, lst):
        try:
            outputs = self.executeAlgorithm(lst)
        except Exception as e:
            raise Exception("User code exception: " + str(e))
        if not self._is_sorted(outputs, lst):
            # raise SortedError(self.__test_name, lst)
            print("Not sorted")
        self.countStackOperations()
        return self.__operation_count

    # def showAnalysisResults(self):
    #     for k in {k: v for k, v in sorted(self.__operation_count.items(), key=lambda item: item[1], reverse=True)}:
    #         print(self.__operation_count[k], dis.opname[k], "code:", k)
