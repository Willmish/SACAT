"""

Note: exception handling is left to the run environment.
The run environment should be able to handle SortedErrors as defined here.

Written by Tim
"""
import timeit

from src.runenv.test_super import SortTest


# A SortedError is raised when a sort algorithm fails
# to sort a list in any test.
class SortedError(Exception):
    def __init__(self, test_name, lst):
        self.__test_name = test_name
        self.__lst = lst

    @property
    def test_name(self):
        return self.__test_name

    @property
    def lst(self):
        return self.__lst


class TimeAnalyser(SortTest):
    def __init__(self, sorting_module, test_name):
        self.__test_name = test_name
        self.__sorting_module = sorting_module

    def analyse(self, lst):
        outputs, run_time = self._single_test(self.__sorting_module.mySort, lst)

        if not self._is_sorted(outputs, lst):
            # raise SortedError(self.__test_name, lst)
            print("Not sorted")
        return run_time
