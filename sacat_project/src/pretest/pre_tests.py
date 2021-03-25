"""
To run the pretests, import your sorting algorithm, initialise a PreTest object
and use the method .run(your_sorting_algorithm). This method will return a string
but the return type can be modified for integration into the final program.

Note: exception handling is left to the run environment.

Written by Tim
"""

from src.runenv.test_super import SortTest
from src.datagen.data_generator import ListGenerator


class PreTest(SortTest):
    def __init__(self, sorting_module):
        self.__sorting_module = sorting_module
        self._lstgen = ListGenerator()
        self.__tests = [
            self._lstgen.random_lst(),  # random list
            [],  # empty list
            self._lstgen.sorted_lst(),  # sorted list
            self._lstgen.reversed_lst(),  # reversed list
            self._lstgen.equal_lst(),  # equal elements list
            self._lstgen.odd_len_lst()  # list of odd length
        ]
        self._test_names = [
            "random list",
            "empty list",
            "sorted list",
            "reverse sorted list",
            "list of equal elements",
            "random list of odd length",
        ]

    # run all tests from self.tests, return processed
    # (hopefully sorted) lists and total time needed
    def __all_tests(self):
        results = []
        times = []
        for lst in self.__tests:
            sorted_lst, time = self._single_test(self.__sorting_module.mySort, lst)
            results.append(self._is_sorted(sorted_lst, lst))
            times.append(time)
        return results, times

    # check whether the processed lists are sorted,
    # return a list of booleans where true stands for sorted
    def __check_results(self, results):
        failed = []
        for i in range(len(results)):
            if not results[i]:
                failed.append(self._test_names[i])
        return failed

    # main method: run tests on a sort algorithm my_sort
    def run(self):
        results, times = self.__all_tests()
        run_time = round(sum(times), 4)
        failed = self.__check_results(results)
        return run_time, failed
        # if len(failed) == 0:
        #     return f"passed all tests in {run_time} s"
        # else:
        #     return f"failed the following tests: {failed}"


# if __name__ == "__main__":
#     pre_test = PreTest()
#     print(pre_test.run(MergeSort.merge_sort))
#     print(pre_test.run(FakeSort.fake_sort))
