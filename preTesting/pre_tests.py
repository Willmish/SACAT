"""
To run the pretests, import your sorting algorithm, initialise a PreTest object
and use the method .run(your_sorting_algorithm). This method will return a string
but the return type can be modified for integration into the final program.

Note: exception handling is left to the run environment.
"""
import random
import timeit
import MergeSort
import FakeSort

class ListGenerator:
  def __init__(self,min_value=-1000000, max_value=1000000, size=100):
    self.__min_value = min_value
    self.__max_value = max_value
    self.__size = size

  # generate a list with random integers
  def random_lst(self):
    lst = [(random.randint(self.__min_value,self.__max_value)) for i in range(self.__size)]
    return lst

  # generate a sorted list of integers
  def sorted_lst(self):
    lst = [i for i in range(self.__size)]
    return lst

  # generate a reverse sorted list of integers
  def reversed_lst(self):
    lst = [i for i in range(self.__size, 0, -1)]
    return lst

  # generate a list of 1s
  def equal_lst(self):
    lst = [1 for i in range(self.__size)]
    return lst
  
  # generate a random list of odd length
  def odd_len_lst(self):
    lst = [(random.randint(self.__min_value,self.__max_value)) for i in range(self.__size-1)]
    return lst

class PreTest:
  def __init__(self):
    self.__lstgen = ListGenerator()
    self.__tests = [
      self.__lstgen.random_lst(),    # random list
      [],                          # empty list
      self.__lstgen.sorted_lst(),    # sorted list
      self.__lstgen.reversed_lst(),  # reversed list
      self.__lstgen.equal_lst(),     # equal elements list
      self.__lstgen.odd_len_lst()    # list of odd length
    ]
    self.__test_names = [
      "random list",
      "empty list",
      "sorted list",
      "reverse sorted list",
      "list of equal elements",
      "random list of odd length",
    ]
  
  # run the sort algorithm on a list and time it
  def __single_test(self, my_sort, lst):
    starttime = timeit.default_timer()
    outputs = my_sort(lst)
    endtime = timeit.default_timer()
    run_time = round(endtime-starttime,4)
    return outputs, run_time

  # run all tests from self.tests, return processed
  # (hopefully sorted) lists and total time needed
  def __all_tests(self,my_sort):
    results = []
    total_time = 0
    for lst in self.__tests:
      sorted_lst, time = self.__single_test(my_sort,lst)
      results.append(self.__is_sorted(sorted_lst, lst))
      total_time += time
    return results, total_time

  # check whether the processed lists are sorted,
  # return a list of booleans where true stands for sorted
  def __check_results(self,results):
    failed = []
    for i in range(len(results)):
      if not results[i]:
        failed.append(self.__test_names[i])
    return failed
  
  # check whether a processed list is the sorted version
  # of another list
  def __is_sorted(self, sorted_lst, lst): 
    return sorted_lst == sorted(lst)
  
  # main method: run tests on a sort algorithm my_sort
  def run(self, my_sort):
    results, run_time = self.__all_tests(my_sort)
    failed = self.__check_results(results)
    if len(failed) == 0:
      return f"passed all tests in {run_time} s"
    else:
      return f"failed the following tests: {failed}"
    
  
if __name__ == "__main__":
  pre_test = PreTest()
  print(pre_test.run(MergeSort.merge_sort))
  print(pre_test.run(FakeSort.fake_sort))