# Take input data (times and array sizes, op count and array sizes, etc.)
# Find best fit complexity with regression (?) {TODO RESEARCH IF A BETTER OPTION EXISTS)
# Use curve fitting (?) TODO CHECK IF BETTER OPTION EXISTS to find approximate equation for the complexity
# Display scatter graph of data and assumed graph along with its complexity
from test_regression import gen_data_return, swap_counter, merge_sort, heapSort, bubblesort
import math
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from scipy.optimize import curve_fit
DEBUG_MODE = True

if DEBUG_MODE:
    print("Welcome!")

def quadratic_objective(x, a, b, c):
    return a * x*x + b * x + c

def score_on_data(data, sizes):
    x = np.array(sizes).reshape((-1,1))
    y = np.array(data)
    model = LinearRegression().fit(x, y)
    return model.score(x, y), model

def get_most_likely_complexity(data, sizes):
    # Returns the most likely complexity (a string) and predicted datapoints
    # For now up to cubic, TODO check if possible to automatically do above cubic
    complexities = [] # stores tuples of (complexity, (fitness, model))
    if DEBUG_MODE:
        print("Begin complexity analysis!")

    # linear
    complexities.append((("n", score_on_data(data, sizes))))
    if DEBUG_MODE:
        print("Linear tested!")

    # logarithmic 
    log_sizes = [math.log(i, 10) for i in sizes]
    complexities.append(("logn", score_on_data(data, log_sizes)))
    if DEBUG_MODE:
        print("logarithmic tested!")

    # Polylogarithmic? (log n)^k

    # linearithmic 
    linlog_sizes = [i*math.log(i, 10) for i in sizes]
    complexities.append(("nlogn", score_on_data(data, linlog_sizes)))
    if DEBUG_MODE:
        print("linearithmic tested!")

    # quasilinear? n (log n)^k

    # quadratic
    quadratic_sizes = [i*i for i in sizes]
    complexities.append(("n2", score_on_data(data, quadratic_sizes)))
    if DEBUG_MODE:
        print("quadratic tested!")

    # cubic 
    cubic_sizes = [i**3 for i in sizes]
    complexities.append(("n3", score_on_data(data, cubic_sizes)))
    if DEBUG_MODE:
        print("cubic tested!")

    # Others? (factorial? non polynomial?)
    
    # Sort according to models score descending order
    complexities = sorted(complexities, key=lambda x: x[1][0], reverse=True)
    if DEBUG_MODE:
        print(complexities)
    
    if complexities[0][0] == "n2":
        predicted_data = complexities[0][1][1].predict(np.array(quadratic_sizes).reshape(-1,1))
        popt, _ = curve_fit(quadratic_objective, sizes, predicted_data)
        a, b, c = popt
        print(a, "n2 + ", b, "n + ", c)
        plot_data(predicted_data, data, sizes, "n2", popt)

def plot_data(predicted_data, data, sizes, complexity, parameters):
    fig, axs = plt.subplots(1, 1)
    fig.suptitle("Bubblesort: Time-size", fontsize=18)
    axs.scatter(sizes, data, s=10, color="green")
    axs.set_xlabel("Array size")
    axs.set_ylabel("Time")
    plt.grid(linestyle='--')
    plt.plot(sizes, predicted_data, label="O(n2) predicted")

    if complexity == "n2": # TODO add other complexities
        a, b, c = parameters 
        new_y = [quadratic_objective(i, a, b ,c) for i in sizes]
    plt.plot(sizes, new_y, label="O(n2) fitted")
    plt.legend()
    plt.show()

time_arr, size_arr, swap_arr = gen_data_return(bubblesort, 4000, 50)

get_most_likely_complexity(time_arr, size_arr)

get_most_likely_complexity(swap_arr, size_arr)

