lines_dict = {n : 0 for n in [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]}




# asadsa





lines_dict[11] += 1
def mergeSort(arr):
    lines_dict[12] += 1
    def partition(arr, low, high):
        lines_dict[13] += 1
        i = (low-1)
        lines_dict[14] += 1
        pivot = arr[high]
        lines_dict[15] += 1
        for j in range(low, high):
            lines_dict[16] += 1
            if arr[j] <= pivot:
                lines_dict[17] += 1
                i = i+1
                lines_dict[18] += 1
                arr[i], arr[j] = arr[j], arr[i]
        lines_dict[19] += 1
        arr[i+1], arr[high] = arr[high], arr[i+1]
        lines_dict[20] += 1
        return (i+1)
    lines_dict[21] += 1
    def quickSort(arr, low, high):
        lines_dict[22] += 1
        if len(arr) == 1:
            lines_dict[23] += 1
            return arr
        lines_dict[24] += 1
        if low < high:
            lines_dict[25] += 1
            pi = partition(arr, low, high)
            lines_dict[26] += 1
            quickSort(arr, low, pi-1)
            lines_dict[27] += 1
            quickSort(arr, pi+1, high)
        lines_dict[28] += 1
        return arr
    lines_dict[29] += 1
    quickSort(arr, 0, len(arr) - 1)


