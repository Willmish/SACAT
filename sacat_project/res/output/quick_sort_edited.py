lines_dict = {n : 0 for n in [2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 21]}
def mySort(arr):
    lines_dict[2] += 1
    def partition(array, low, high):
        lines_dict[3] += 1
        i = (low-1)
        lines_dict[4] += 1
        pivot = array[high]
        lines_dict[5] += 1
        for j in range(low, high):
            lines_dict[6] += 1
            if array[j] <= pivot:
                lines_dict[7] += 1
                i = i+1
                lines_dict[8] += 1
                array[i], array[j] = array[j], array[i]
        lines_dict[9] += 1
        array[i+1], array[high] = array[high], array[i+1]
        lines_dict[10] += 1
        return i+1

    lines_dict[12] += 1
    def quickSort(array, low, high):
        lines_dict[13] += 1
        if len(array) == 1:
            lines_dict[14] += 1
            return array
        lines_dict[15] += 1
        if low < high:
            lines_dict[16] += 1
            pi = partition(array, low, high)
            lines_dict[17] += 1
            quickSort(array, low, pi-1)
            lines_dict[18] += 1
            quickSort(array, pi+1, high)
        lines_dict[19] += 1
        return array

    lines_dict[21] += 1
    return quickSort(arr, 0, len(arr) - 1)


