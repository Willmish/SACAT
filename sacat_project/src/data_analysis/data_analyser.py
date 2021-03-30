# Written by Szymon Duchniewicz March, 2021
'''
DataAnalyser class encapsulates all methods used for the estimation of time complexity based on 
data passed to it.

To analyse data, create an instance of DataAnalyser and pass it dependant data (running time/operation counts) 
and array sizes. Then call get_most_likely_complexity() method. Optionally, call plot_data() to display the 
current best-fit complexity and its curve. (note that DEBUG_MODE constant must be set to true in order for
plot_data() method to work.)

'''
# Take input data (times and array sizes, op count and array sizes, etc.)
# Find best fit complexity with regression (?) {TODO RESEARCH IF A BETTER OPTION EXISTS)
# Use curve fitting (?) TODO CHECK IF BETTER OPTION EXISTS to find approximate equation for the complexity
# Display scatter graph of data and assumed graph along with its complexity
from typing import List, Tuple
from src.data_analysis.objective_functions import ObjectiveFunctions
from src.data_analysis.results_storage import ResultsStorage
from src.runenv.run_environment import TestStorage

from math import log
import numpy as np
from sklearn.linear_model import LinearRegression
from scipy.optimize import curve_fit


DEBUG_MODE = False
if DEBUG_MODE:
    # optional imports used for debugging (necessary for plot_data() method)
    from src.data_analysis.test_regression import gen_data_return, swap_counter, merge_sort, heapSort, bubblesort
    import matplotlib.pyplot as plt

if DEBUG_MODE:
    print("Welcome!")

class DataAnalyser:
    # TODO cahange so that it receives TestStorage as input
    def __init__(self, testStorages: List[TestStorage]):
        self.data = []
        self.sizes = []
        self.random_test_storage = None
        self.duplicate_test_storage = None
        self.sorted_test_storage = None
        self.reversed_test_type = None
        for storage in testStorages:
            if storage.test_type == "random":
                self.random_test_storage = storage
            elif storage.test_type == "duplicate":
                self.duplicate_test_storage = storage
            elif storage.test_type == "sorted":
                self.sorted_test_storage = storage
            elif storage.test_type == "reversed":
                self.reversed_test_type = storage
            else:
                raise Exception("TestStorage type not recognised by DataAnalyser!")

        self.complexity: str = ""
        self.complexities: List[Tuple] = []

    def set_data(self, new_data: List):
        self.data = new_data

    def set_sizes(self, new_sizes: List):
        self.sizes = new_sizes

    def full_data_analysis(self):
        storages = []
        if self.random_test_storage is None:
            storages.append(None)
        else:
            storages.append(self.test_on_storage(self.random_test_storage))
        if self.duplicate_test_storage is None:
            storages.append(None)
        else:
            storages.append(self.test_on_storage(self.duplicate_test_storage))
        if self.sorted_test_storage is None:
            storages.append(None)
        else:
            storages.append(self.test_on_storage(self.sorted_test_storage))
        if self.reversed_test_type is None:
            storages.append(None)
        else:
            storages.append(self.test_on_storage(self.reversed_test_type))
        return storages

    def test_on_storage(self, storage: TestStorage):
        # TODO IMPORTANT NOTE: FOR SPACE ANALYSIS NEED DIFFERENT METHOD
        result_storage = ResultsStorage(storage.test_type)
        self.set_sizes(storage.sizes)
        if storage.times[0] is not None:
            self.set_data(storage.times)
            result_storage.times_results = self.get_most_likely_complexity()
        else:
            result_storage.times_results = None
        if storage.operations[0] is not None:
            self.set_data(storage.operations)
            result_storage.operations_results = self.get_most_likely_complexity()
        else:
            result_storage.operations_results = None
        if storage.spaces[0] is not None:
            self.set_data(storage.spaces)
            result_storage.space_results = self.get_most_likely_complexity()
        else:
            result_storage.space_results = None
        return result_storage


    def score_on_data(self, data, sizes):
        x = np.array(sizes).reshape((-1,1))
        y = np.array(data)
        model = LinearRegression().fit(x, y)
        return model.score(x, y), model

    def get_most_likely_complexity(self):
        # Returns a Tuple of (Most_likely_complexity: string, (optimum_parameters: Tuple[float, ...]), predicted_data: List, data: List, sizes: List)
        # For now up to cubic, TODO check if possible to automatically do above cubic
        self.complexities = [] # stores tuples of (complexity, (fitness, model))
        if DEBUG_MODE:
            print("Begin complexity analysis!")

        # logarithmic 
        log_sizes = [log(i, 10) for i in self.sizes]
        self.complexities.append(("logn", self.score_on_data(self.data, log_sizes)))
        if DEBUG_MODE:
            print("logarithmic tested!")

        # linear
        self.complexities.append((("n", self.score_on_data(self.data, self.sizes))))
        if DEBUG_MODE:
            print("Linear tested!")

        # Polylogarithmic? (log n)^k

        # linearithmic 
        linlog_sizes = [i*log(i, 10) for i in self.sizes]
        self.complexities.append(("nlogn", self.score_on_data(self.data, linlog_sizes)))
        if DEBUG_MODE:
            print("linearithmic tested!")

        # quasilinear? n (log n)^k

        # quadratic
        quadratic_sizes = [i*i for i in self.sizes]
        self.complexities.append(("n2", self.score_on_data(self.data, quadratic_sizes)))
        if DEBUG_MODE:
            print("quadratic tested!")

        # cubic 
        cubic_sizes = [i**3 for i in self.sizes]
        self.complexities.append(("n3", self.score_on_data(self.data, cubic_sizes)))
        if DEBUG_MODE:
            print("cubic tested!")

        # Others? (factorial? non polynomial?)
        
        # Sort according to models score descending order
        self.complexities = sorted(self.complexities, key=lambda x: x[1][0], reverse=True)
        most_likely_complexity = self.complexities[0][0]
        if DEBUG_MODE:
            print(self.complexities)
        
        if most_likely_complexity == "logn":
            predicted_data = self.complexities[0][1][1].predict(np.array(log_sizes).reshape(-1,1))
            popt, _ = curve_fit(ObjectiveFunctions.logarithmic_objective, self.sizes, predicted_data)
            if DEBUG_MODE:
                b, c = popt
                print(b, "logn + ", c)
                self.plot_data(predicted_data, self.data, self.sizes, most_likely_complexity, popt)
            return most_likely_complexity, popt, predicted_data, self.data, self.sizes  

        if most_likely_complexity == "n":
            predicted_data = self.complexities[0][1][1].predict(np.array(self.sizes).reshape(-1,1))
            popt, _ = curve_fit(ObjectiveFunctions.linear_objective, self.sizes, predicted_data)
            if DEBUG_MODE:
                b, c = popt
                print(b, "n + ", c)
                self.plot_data(predicted_data, self.data, self.sizes, most_likely_complexity, popt)
            return most_likely_complexity, popt, predicted_data, self.data, self.sizes  

        if most_likely_complexity == "nlogn":
            predicted_data = self.complexities[0][1][1].predict(np.array(linlog_sizes).reshape(-1,1))
            popt, _ = curve_fit(ObjectiveFunctions.linearithmic_objective, self.sizes, predicted_data)
            if DEBUG_MODE:
                a, b, c = popt
                print(a, "nlogn + ", b, "n + ", c)
                self.plot_data(predicted_data, self.data, self.sizes, most_likely_complexity, popt)
            return most_likely_complexity, popt, predicted_data, self.data, self.sizes  

        if most_likely_complexity == "n2":
            predicted_data = self.complexities[0][1][1].predict(np.array(quadratic_sizes).reshape(-1,1))
            print(predicted_data)
            popt, _ = curve_fit(ObjectiveFunctions.quadratic_objective, self.sizes, predicted_data)
            if DEBUG_MODE:
                a, b, c = popt
                print(a, "n2 + ", b, "n + ", c)
                self.plot_data(predicted_data, self.data, self.sizes, most_likely_complexity, popt)
            return most_likely_complexity, popt, predicted_data, self.data, self.sizes  

        if most_likely_complexity == "n3":
            predicted_data = self.complexities[0][1][1].predict(np.array(cubic_sizes).reshape(-1,1))
            popt, _ = curve_fit(ObjectiveFunctions.cubic_objective, self.sizes, predicted_data)
            if DEBUG_MODE:
                a, b, c, d = popt
                print(a, "n3 + ", b, "n2 + ", c, "n + ", d)
                self.plot_data(predicted_data, self.data, self.sizes, most_likely_complexity, popt)
            return (most_likely_complexity, popt, predicted_data, self.data, self.sizes) # TODO data type for results (4 data storages, each with 4 tests to analyse)

    def plot_data(self, predicted_data, data, sizes, complexity, parameters):
        fig, axs = plt.subplots(1, 1)
        fig.suptitle("Some algo", fontsize=18)
        axs.scatter(sizes, data, s=10, color="green")
        axs.set_xlabel("Array size")
        axs.set_ylabel("Dependant")
        plt.grid(linestyle='--')
        plt.plot(sizes, predicted_data, label=f"O({complexity}) predicted")

        if complexity == "logn":
            a, b = parameters 
            new_y = [ObjectiveFunctions.logarithmic_objective(i, a, b) for i in sizes]

        if complexity == "n":
            a, b = parameters 
            new_y = [ObjectiveFunctions.linear_objective(i, a, b) for i in sizes]

        if complexity == "nlogn":
            a, b, c = parameters 
            new_y = [ObjectiveFunctions.linearithmic_objective(i, a, b, c) for i in sizes]

        if complexity == "n2": # TODO add other complexities
            a, b, c = parameters 
            new_y = [ObjectiveFunctions.quadratic_objective(i, a, b ,c) for i in sizes]

        if complexity == "n3":
            a, b, c, d = parameters 
            new_y = [ObjectiveFunctions.cubic_objective(i, a, b, c, d) for i in sizes]
        plt.plot(sizes, new_y, label=f"O({complexity}) fitted")
        plt.legend()
        plt.show()

if __name__ == "__main__":
    time_arr, size_arr, swap_arr = gen_data_return(heapSort, 10000, 50)
    data_analyser = DataAnalyser(time_arr, size_arr)

    data_analyser.get_most_likely_complexity()

    time_arr, size_arr, swap_arr = gen_data_return(merge_sort, 10000, 50)
    data_analyser.set_data(time_arr)
    data_analyser.set_sizes(size_arr)
    data_analyser.get_most_likely_complexity()
    #data_analyser.set_data(swap_arr)
    #data_analyser.get_most_likely_complexity()

