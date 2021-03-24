"""

Note: exception handling is left to the run environment.
The run environment should be able to handle SortedErrors as defined here.

Written by Tim
"""

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
    def __init__(self, test_name):
        self.__test_name = test_name
        # self._t_max = t_max
        # self._tests = [
        #   self._lstgen.random_lst(),    # random list
        #   self._lstgen.duplicate_lst(), # duplicate list
        #   self._lstgen.sorted_lst(),    # sorted list
        #   self._lstgen.reversed_lst(),  # reversed list
        # ]
        # self._test_names = [
        #   "random list",
        #   "duplicate list",
        #   "sorted list",
        #   "reverse sorted list",
        # ]

    # # Run a group of tests, return (size, run_time) list.
    # # Basic time keeping ends the testing after a test takes
    # # longer than t_max.
    # def __group_of_tests(self, my_sort, generator_function, test_name):
    #   default_size = self._lstgen.size
    #   run_time = 0
    #   results = []
    #   i = 1
    #   while(run_time < self._t_max):
    #     lst = generator_function()
    #     sorted_lst, run_time = self._single_test(my_sort,lst)
    #     # if a list is not sorted immediately raise an error
    #     # and abort the group of tests
    #     if not self.__is_sorted(sorted_lst, lst):
    #       raise SortedError(test_name)
    #     results.append(self._lstgen.size, run_time)
    #     self._lstgen.size = 10 ** (0.1 * i)
    #     i += 1
    #   self._lstgen.size = default_size
    #   return results

    def analyse(self, my_sort, lst):
        outputs, run_time = self._single_test(my_sort, lst)
        if not self._is_sorted(outputs, lst):
            # raise SortedError(self.__test_name, lst)
            print("Not sorted")
        return run_time
