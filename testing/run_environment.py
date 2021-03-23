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

  def run(self, my_sort):
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(10)   # Ten seconds
    try:
        long_function_call()
    except Exception, msg:
        print "Timed out!"
  
  def run_random(self, my_sort):
    test_count = 0
    while(test_count < self.max_tests):
      lst_gen.size = self.lst_size
      lst_gen.random_lst()
      
      #TODO is this the right way to increase the size?
      self.lst_size += self.step
      test_count += 1


  def run_all_tests(self, my_sort, lst):
    return run_test_time(), run_test_operations(), run_test_space()

  def run_test_time(self, my_sort, lst):
    pass

  def run_test_operations(self, my_sort, lst):
    pass

  def run_test_space(self, my_sort, lst):
    pass
