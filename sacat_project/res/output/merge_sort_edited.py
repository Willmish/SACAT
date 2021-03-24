lines_dict = {n : 0 for n in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]}
def mySort(arr):
    lines_dict[2] += 1
    if len(arr) > 1:
        lines_dict[3] += 1
        mid = len(arr)//2
        lines_dict[4] += 1
        L = arr[:mid]
        lines_dict[5] += 1
        R = arr[mid:]
        lines_dict[6] += 1
        mySort(L)
        lines_dict[7] += 1
        mySort(R)
        lines_dict[8] += 1
        i = j = k = 0
        lines_dict[9] += 1
        while i < len(L) and j < len(R):
            lines_dict[10] += 1
            if L[i] < R[j]:
                lines_dict[11] += 1
                arr[k] = L[i]
                lines_dict[12] += 1
                i += 1
            else:
                lines_dict[14] += 1
                arr[k] = R[j]
                lines_dict[15] += 1
                j += 1
            lines_dict[16] += 1
            k += 1
        lines_dict[17] += 1
        while i < len(L):
            lines_dict[18] += 1
            arr[k] = L[i]
            lines_dict[19] += 1
            i += 1
            lines_dict[20] += 1
            k += 1
        lines_dict[21] += 1
        while j < len(R):
            lines_dict[22] += 1
            arr[k] = R[j]
            lines_dict[23] += 1
            j += 1
            lines_dict[24] += 1
            k += 1
    lines_dict[25] += 1
    return arr

