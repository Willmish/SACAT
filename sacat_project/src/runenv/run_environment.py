from src.datagen.data_generator import ListGenerator
from src.runenv.op_analysis import OpAnalyzer
from src.runenv.time_analysis import TimeAnalyser


class TestStorage():
    def __init__(self, test_type):
        self.test_type = test_type
        self.sizes = []
        self.times = []
        self.operations = []
        self.spaces = []
        self.length = 0

    # TODO consider cases where we only test one or two things to analyse, e.g. only time
    def append(self, size, time, operations, space):
        self.sizes.append(size)
        self.times.append(time)
        self.operations.append(operations)
        self.spaces.append(space)
        self.length += 1

    def __str__(self):
        result = ""
        result += self.test_type
        result += "\n"
        for i in range(self.length):
            result += "Size : " + str(self.sizes[i]) + " Time : " + str(self.times[i]) + " Operations : " + str(
                self.operations[i]) + " Space : " + str(self.spaces[i])
            result += "\n"
        return result


class RunEnvironment():
    # TODO default values for t_max etc.?
    def __init__(self, unparsedModule, parsedModule, op_table, t_max=1, T_max=10, max_tests=10, step=100):
        self.__unparsedModule = unparsedModule
        self.__parsedModule = parsedModule
        self.__op_table = op_table
        self.t_max = t_max
        self.T_max = T_max
        self.max_tests = max_tests
        self.step = step
        self.lst_size = 1
        self.lst_gen = ListGenerator(size=self.lst_size)
        self.test_sizes = []
        self.test_output = []

    # def signal_handler(signum, frame):
    #   raise Exception("Timed out!")

    # def run_signal(self, my_sort):
    #   signal.signal(signal.SIGALRM, signal_handler)
    #   signal.alarm(10)   # Ten seconds
    #   try:
    #       long_function_call()
    #   except Exception, msg:
    #       print "Timed out!"

    def run(self, time_analysis: bool, operations_analysis: bool, space_analysis: bool, random: bool,
            duplicate: bool, sortedd: bool, reversedd: bool):
        storage_lst = []
        if random:
            storage_lst.append(
                self.run_with_generator(self.lst_gen.random_lst, "random", time_analysis, operations_analysis,
                                        space_analysis))
        if duplicate:
            storage_lst.append(self.run_with_generator(self.lst_gen.duplicate_lst, "duplicate", time_analysis,
                                                       operations_analysis, space_analysis))
        if sortedd:
            storage_lst.append(
                self.run_with_generator(self.lst_gen.sorted_lst, "sorted", time_analysis, operations_analysis,
                                        space_analysis))
        if reversedd:
            storage_lst.append(self.run_with_generator(self.lst_gen.reversed_lst, "reversed", time_analysis,
                                                       operations_analysis, space_analysis))
        return storage_lst

    def run_with_generator(self, generator, test_type, time_analysis: bool, operations_analysis: bool,
                           space_analysis: bool):
        test_count = 0
        time_analyser = TimeAnalyser(test_type)
        operations_analyser = OpAnalyzer(self.__parsedModule, self.__op_table, test_type)
        storage = TestStorage(test_type)
        while test_count < self.max_tests:
            self.lst_gen.size = self.lst_size
            lst = generator()
            size = len(lst)
            time, operations, space = None, None, None
            if time_analysis:
                time = self.run_test_time(lst, time_analyser)
            if operations_analysis:
                operations = self.run_test_operations(lst, operations_analyser)
            if space_analysis:
                space = self.run_test_space(lst)
            storage.append(size, time, operations, space)
            # TODO is this the right way to increase the size?
            self.lst_size += self.step
            test_count += 1
        self.lst_size = 1
        return storage

    def run_test_time(self, lst, time_analyser):
        return time_analyser.analyse(self.__unparsedModule.mySort, lst)

    def run_test_operations(self, lst, operations_analyser):
        return operations_analyser.analyse(lst)
        # return None

    def run_test_space(self, lst):
        return None


# if __name__ == "__main__":
#     re = RunEnvironment()
#     results = re.run(MergeSort.merge_sort, True, False, False, True, True, True, True)
#     for storage in results:
#         print(storage)
