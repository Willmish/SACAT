import signal
from data_generator import ListGenerator

class TestStorage():
  def __init__(self, test_type):
    self.test_type = test_type
    self.sizes = []
    self.times = []
    self.operations = []
    self.spaces = []
  
  #TODO consider cases where we only test one or two things to analyse, e.g. only time
  def append(size, time, operations, space):
    self.sizes.append(size)
    self.times.append(time)
    self.operations.append(operations)
    self.spaces.append(space)

class RunEnvironment():
  def __init__(self, t_max, T_max, max_tests = 1000, step = 10):
    self.t_max = t_max
    self.T_max = T_max
    self.max_tests = max_tests
    self.step = step
    self.lst_size = 1
    self.lst_gen = ListGenerator(size = self.lst_size)
    self.test_sizes = []
    self.test_output = []

  def signal_handler(signum, frame):
    raise Exception("Timed out!")

  def run_signal(self, my_sort):
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(10)   # Ten seconds
    try:
        long_function_call()
    except Exception, msg:
        print "Timed out!"
  
  def run(self, my_sort, time_analysis:bool, operations_analysis:bool, space_analysis:bool, random:bool, duplicate:bool, sortedd:bool, reversedd:bool):
    storage_lst = []
    if random:
      storage_lst.append(run_with_generator(my_sort, self.lst_gen.random_lst, "random", time_analysis, operations_analysis, space_analysis))
    if duplicate:
      storage_lst.append(run_with_generator(my_sort, self.lst_gen.duplicate_lst, "duplicate", time_analysis, operations_analysis, space_analysis))
    if sortedd:
      storage_lst.append(run_with_generator(my_sort, self.lst_gen.sorted_lst, "sorted", time_analysis, operations_analysis, space_analysis))
    if reversedd:
      storage_lst.append(run_with_generator(my_sort, self.lst_gen.reversed_lst, "reversed", time_analysis, operations_analysis, space_analysis))
    return storage_lst

  def run_with_generator(self, my_sort, generator, test_type, time_analysis:bool, operations_analysis:bool, space_analysis:bool):
    test_count = 0
    storage = TestStorage(test_type)
    while(test_count < self.max_tests):
      self.lst_gen.size = self.lst_size
      lst = generator()
      size = len(lst)
      time, operations, space = None, None, None
      if time_analysis:
        time = run_test_time(my_sort, lst)
      if operations_analysis:
        operations = run_test_operations(my_sort, lst)
      if space_analysis:
        operations = run_test_space(my_sort, lst)
      storage.append(size, time, operations, space)
      #TODO is this the right way to increase the size?
      self.lst_size += self.step
      test_count += 1
    self.lst_size = 1
    return storage

  def run_test_time(self, my_sort, lst):
    pass

  def run_test_operations(self, my_sort, lst):
    pass

  def run_test_space(self, my_sort, lst):
    pass

