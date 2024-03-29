"""
Space complexity analysis module.

Written by Andrzej Szablewski, March 2021.
"""

import random
import tracemalloc as tm

from src.runenv.test_super import SortTest


class SpaceAnalyzer(SortTest):
    def __init__(self, sorting_module, test_name):
        self.__sorting_module = sorting_module
        self.__test_name = test_name

    def analyse(self, lst):
        tm.clear_traces()
        tm.start()
        random.shuffle(lst)
        try:
            output = self.__sorting_module.mySort(lst)
        except Exception as e:
            raise Exception("User code exception: " + str(e))

        _, peak = tm.get_traced_memory()
        if not self._is_sorted(output, lst):
            # raise SortedError(self.__test_name, lst)
            print("Not sorted")
        tm.stop()
        return peak


