import tracemalloc as tm
import random 
import importlib.util

def mergeSort(arr):
    if len(arr) > 1:
        mid = len(arr)//2
        L = arr[:mid]
        R = arr[mid:]
        mergeSort(L)
        mergeSort(R)
        i = j = k = 0
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1
    return arr

arr = [random.randint(-100000, 100000) for x in range(1000000)]

# tm.clear_traces()
# tm.start(100)
# print(tm.get_traced_memory())

# abc = mergeSort(arr)
# print(tm.get_traced_memory())


# tm.clear_traces()

# print(tm.get_traced_memory())
# abc = mergeSort(arr)

class SpaceAnalysis:
    def __init__(self, fileFrom):
        self.__sorting_module = self.__importModule(fileFrom)
        pass

    @staticmethod
    def __importModule(filepath):
        spec = importlib.util.spec_from_file_location(filepath, filepath)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def analyse(self, arr):
        tm.clear_traces()
        tm.start()
        output = self.__sorting_module.mySort(arr)
        _, peak = tm.get_traced_memory()
        tm.clear_traces()
        tm.stop()
        return peak
        
sa = SpaceAnalysis("./parser/res/input/mergeSort.py")
print(sa.analyse(arr) / 1024, "KiB")
