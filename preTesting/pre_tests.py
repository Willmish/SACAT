import random
import timeit
import MergeSort
import FakeSort

class ListGenerator:
  def __init__(self,min_value=-1000000, max_value=1000000, size=100):
    self.min_value = min_value
    self.max_value = max_value
    self.size = size

  # generate a list with random integers
  def random_lst(self):
    lst = [(random.randint(self.min_value,self.max_value)) for i in range(self.size)]
    return lst

  # generate a sorted list of integers
  def sorted_lst(self):
    lst = [i for i in range(self.size)]
    return lst

  # generate a reverse sorted list of integers
  def reversed_lst(self):
    lst = [i for i in range(self.size, 0, -1)]
    return lst

  # generate a list of 1s
  def equal_lst(self):
    lst = [1 for i in range(self.size)]
    return lst
  
  # generate a random list of odd length
  def odd_len_lst(self):
    lst = [(random.randint(self.min_value,self.max_value)) for i in range(self.size-1)]
    return lst

class PreTest:
  def __init__(self):
    self.lstgen = ListGenerator()
    self.tests = [
      self.lstgen.random_lst(),    # random list
      [],                          # empty list
      self.lstgen.sorted_lst(),    # sorted list
      self.lstgen.reversed_lst(),  # reversed list
      self.lstgen.equal_lst(),     # equal elements list
      self.lstgen.odd_len_lst()    # list of odd length
    ]
    self.test_names = [
      "random list",
      "empty list",
      "sorted list",
      "reverse sorted list",
      "list of equal elements",
      "random list of odd length",
    ]
  
  def single_test(self, my_sort, lst):
    starttime = timeit.default_timer()
    outputs = my_sort(lst)
    endtime = timeit.default_timer()
    run_time = round(endtime-starttime,4)
    return outputs, run_time

  def all_tests(self,my_sort):
    results = []
    total_time = 0
    for lst in self.tests:
      sorted_lst, time = self.single_test(my_sort,lst)
      results.append(self.is_sorted(sorted_lst, lst))
      total_time += time
    return results, total_time

  def check_results(self,results):
    failed = []
    for i in range(len(results)):
      if not results[i]:
        failed.append(self.test_names[i])
    return failed
  
  def is_sorted(self, sorted_lst, lst): 
    return sorted_lst == sorted(lst)
  
  def run(self, my_sort):
    results, run_time = self.all_tests(my_sort)
    failed = self.check_results(results)
    if len(failed) == 0:
      return f"passed all tests in {run_time} s"
    else:
      return f"failed the following tests: {failed}"
    
  
if __name__ == "__main__":
  pre_test = PreTest()
  print(pre_test.run(MergeSort.merge_sort))
  print(pre_test.run(FakeSort.fake_sort))