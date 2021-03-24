"""
SortTest is an abstract base class for PreTest and TimeAnalyser objects. 
It provides methods for 
- running and timing a test,
- checking whether results from a test a sorted.

Note: exception handling is left to the run environment.

Written by Tim
"""

import timeit
from abc import ABC


class SortTest(ABC):
    # run the sort algorithm on a list and time it
    def _single_test(self, my_sort, lst):
        starttime = timeit.default_timer()
        outputs = my_sort(lst)
        endtime = timeit.default_timer()
        run_time = endtime - starttime
        return outputs, run_time

    # check whether a processed list is the sorted version
    # of another list
    def _is_sorted(self, sorted_lst, lst):
        return sorted_lst == sorted(lst)
