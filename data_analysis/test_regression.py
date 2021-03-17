import matplotlib.pyplot as plt
from time import time
import random
import math
import numpy as np
from sklearn.linear_model import LinearRegression
# FROM ROSETTA CODE
from heapq import merge

swap_counter = 0

def merge_sort(m):
    if len(m) <= 1:
        return m

    middle = len(m) // 2
    left = m[:middle]
    right = m[middle:]

    left = merge_sort(left)
    right = merge_sort(right)
    return list(merge(left, right))
def heapify(arr, n, i):
    largest = i  # Initialize largest as root
    l = 2 * i + 1     # left = 2*i + 1
    r = 2 * i + 2     # right = 2*i + 2
 
    # See if left child of root exists and is
    # greater than root
    if l < n and arr[largest] < arr[l]:
        largest = l
 
    # See if right child of root exists and is
    # greater than root
    if r < n and arr[largest] < arr[r]:
        largest = r
 
    # Change root, if needed
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]  # swap
 
        # Heapify the root.
        heapify(arr, n, largest)
 
# The main function to sort an array of given size
 
 
def heapSort(arr):
    n = len(arr)
    global swap_counter 
 
    # Build a maxheap.
    for i in range(n//2 - 1, -1, -1):
        heapify(arr, n, i)
 
    # One by one extract elements
    for i in range(n-1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]  # swap
        swap_counter += 1 
        heapify(arr, i, 0)
# ------------------

def linear_search(arr):
    for i in arr:
        if -1 == i:
            return True
    return False


def bubblesort(arr):
    global swap_counter
    swap_counter = 0
    if isinstance(arr, str):
        arr = list(arr)
    swap = None
    swap_ocurred = False
    for i in range(len(arr)):
        for j in range(len(arr)-i-1):
            swap_counter += 1
            if arr[j+1] < arr[j]:
                swap = arr[j+1]
                arr[j+1] = arr[j]
                arr[j] = swap
                swap_ocurred = True
        if not swap_ocurred:
            break
    return arr



def gen_data(algo_func, time_arr, size_arr, swap_arr):
    test_arr = []
    global swap_counter
    max_size = 4000
    for i in range(1, max_size, max_size//50):
        size_arr.append(i)
        test_arr = [random.random() for _ in range(i)]

        time_b = time()
        algo_func(test_arr)
        time_arr.append((time()-time_b))
        swap_arr.append(swap_counter)
    print(swap_arr)


time_arr_lin = []
size_arr_lin = []
swap_arr_lin = []

time_arr_bub = []
size_arr_bub = []
swap_arr_bub = []

time_arr_merg = []
size_arr_merg = []
swap_arr_merg = []

time_arr_heap = []
size_arr_heap = []
swap_arr_heap = []

#gen_data(linear_search, time_arr_lin, size_arr_lin, swap_arr_lin)
gen_data(merge_sort, time_arr_merg, size_arr_merg, swap_arr_merg)
gen_data(bubblesort, time_arr_bub, size_arr_bub, swap_arr_bub)
gen_data(heapSort, time_arr_heap, size_arr_heap, swap_arr_heap)



#plt.plot(size_arr_lin, time_arr_lin)
plt.show()
fig, axs = plt.subplots(1, 1)
axs.plot(size_arr_merg, time_arr_merg, solid_joinstyle='round')
axs.set_title("Mergesort")
axs.set_xlabel("Array size")
axs.set_ylabel("Time")
plt.grid(linestyle='--')
plt.show()
fig, axs = plt.subplots(1, 1)
axs.plot(size_arr_heap, time_arr_heap)
axs.set_title("Heapsort")
axs.set_xlabel("Array size")
axs.set_ylabel("Time")
plt.grid(linestyle='--')
plt.show()

fig, axs = plt.subplots(1, 1)
fig.suptitle("Bubblesort: Time-size", fontsize=18)
axs.plot(size_arr_bub, time_arr_bub)
axs.set_xlabel("Array size")
axs.set_ylabel("Time")
plt.grid(linestyle='--')
plt.show()

fig, axs = plt.subplots(1, 1)
axs.plot(size_arr_bub, swap_arr_bub)
axs.set_title("Bubblesort: Comparisons-size")
axs.set_xlabel("Array size")
axs.set_ylabel("No. comparisons")
plt.grid(linestyle='--')
plt.show()
#plt.plot(size_arr_bub, time_arr_bub)
#plt.plot(size_arr_bub, swap_arr_bub)
'''
# analyse
x = np.array(time_arr_lin).reshape((-1,1))
y = np.array(size_arr_lin)

model = LinearRegression().fit(x, y)
print("Linear search O(n) fit: ", model.score(x, y))
'''
# analyse BUBBLE
x = np.array(time_arr_bub).reshape((-1,1))
y = np.array(size_arr_bub)

model = LinearRegression().fit(x,y)
print("Bubblesort (time) O(n) fit: ", model.score(x, y))
# analyse
size_arr_bub_log = [i*math.log(i) for i in size_arr_bub]
x = np.array(time_arr_bub).reshape((-1,1))
y = np.array(size_arr_bub_log)

model = LinearRegression().fit(x,y)
print("Bubblesort (time) O(nlogn) fit: ", model.score(x, y))

# analyse
size_arr_bub_sqr = [i**2 for i in size_arr_bub]
x = np.array(time_arr_bub).reshape((-1,1))
y = np.array(size_arr_bub_sqr)

model = LinearRegression().fit(x,y)
print("Bubblesort (time) O(n2) fit: ", model.score(x, y))

<<<<<<< HEAD:test_regression.py
'''
=======
# ANALYSE COMPARISONS
x = np.array(swap_arr_bub).reshape((-1, 1))
y = np.array(size_arr_bub)

model = LinearRegression().fit(x,y)
print("Bubblesort (Comparisons) O(n) fit: ", model.score(x, y))
# analyse
x = np.array(swap_arr_bub).reshape((-1,1))
y = np.array(size_arr_bub_log)

model = LinearRegression().fit(x,y)
print("Bubblesort (Comparisons) O(nlogn) fit: ", model.score(x, y))

# analyse
x = np.array(swap_arr_bub).reshape((-1,1))
y = np.array(size_arr_bub_sqr)

model = LinearRegression().fit(x,y)
print("Bubblesort (Comparisons) O(n2) fit: ", model.score(x, y))
# ____________________________________________________________________
>>>>>>> Prettify graphs for raport.:data_analysis/test_regression.py
# analyse MERGESORT 
x = np.array(time_arr_merg).reshape((-1,1))
y = np.array(size_arr_merg)

model = LinearRegression().fit(x,y)
print("MErgesort O(n) fit: ", model.score(x, y))

# analyse
size_arr_merg_log = [i*math.log(i) for i in size_arr_merg]
x = np.array(time_arr_merg).reshape((-1,1))
y = np.array(size_arr_merg_log)

model = LinearRegression().fit(x,y)
print("MErgesort O(nlogn) fit: ", model.score(x, y))

# analyse
size_arr_merg_sqr = [(i*i) for i in size_arr_merg]
x = np.array(time_arr_merg).reshape((-1,1))
y = np.array(size_arr_merg_sqr)

model = LinearRegression().fit(x,y)
print("MErgesort O(n2) fit: ", model.score(x, y))



# analyse HEAPSORT
x = np.array(time_arr_heap).reshape((-1,1))
y = np.array(size_arr_heap)

model = LinearRegression().fit(x,y)
print("Heapsort O(n) fit: ", model.score(x, y))

# analyse
size_arr_heap_log = [i*math.log(i) for i in size_arr_heap]
x = np.array(time_arr_heap).reshape((-1,1))
y = np.array(size_arr_heap_log)

model = LinearRegression().fit(x,y)
print("Heapsort O(nlogn) fit: ", model.score(x, y))

# analyse
size_arr_heap_sqr = [i*i for i in size_arr_heap]
x = np.array(time_arr_heap).reshape((-1,1))
y = np.array(size_arr_heap_sqr)

model = LinearRegression().fit(x,y)
print("Heapsort O(n2) fit: ", model.score(x, y))
'''
