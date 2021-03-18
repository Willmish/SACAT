



# asadsa





def mySort(arr):
    
    def partition(arr, low, high):
        try:
            i = (low-1)
            pivot = arr[high]
            for j in range(low, high):
                if arr[j] <= pivot:
                    i = i+1
                    arr[i], arr[j] = arr[j], arr[i]
            arr[i+1], arr[high] = arr[high], arr[i+1]
        except Exception as e:
            pass
        return (i+1)
        
        # asdasdasdas
    def quickSort(arr, low, high):
        if len(arr) == 1:
            return arr



        if low < high:
            pi = partition(arr, low, high)
            quickSort(arr, low, pi-1)
            quickSort(arr, pi+1, high)
        return arr
    quickSort(arr, 0, len(arr) - 1)
    return arr
