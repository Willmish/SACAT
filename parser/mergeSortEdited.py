lines_list = [0 for x in range(23)]
def mergeSort(arr):
    lines_list[0] += 1
    if len(arr) > 1:
        lines_list[1] += 1
        mid = len(arr)//2
        lines_list[2] += 1
        L = arr[:mid]
        lines_list[3] += 1
        R = arr[mid:]
        lines_list[4] += 1
        mergeSort(L)
        lines_list[5] += 1
        mergeSort(R)
        lines_list[6] += 1
        i = j = k = 0
        lines_list[7] += 1
        while i < len(L) and j < len(R):
            lines_list[8] += 1
            if L[i] < R[j]:
                lines_list[9] += 1
                arr[k] = L[i]
                lines_list[10] += 1
                i += 1
            else:
                lines_list[11] += 1
                arr[k] = R[j]
                lines_list[12] += 1
                j += 1
            lines_list[13] += 1
            k += 1
        lines_list[14] += 1
        while i < len(L):
            lines_list[15] += 1
            arr[k] = L[i]
            lines_list[16] += 1
            i += 1
            lines_list[17] += 1
            k += 1
        lines_list[18] += 1
        while j < len(R):
            lines_list[19] += 1
            arr[k] = R[j]
            lines_list[20] += 1
            j += 1
            lines_list[21] += 1
            k += 1
    lines_list[22] += 1
    return arr

