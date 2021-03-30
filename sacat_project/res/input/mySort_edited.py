lines_dict = {n: 0 for n in [2, 3, 4, 5, 6, 7, 8, 10]}
def mySort(arr):
    lines_dict[2] += 1
    for i in range(1, len(arr)):
        lines_dict[3] += 1
        key = arr[i]
        lines_dict[4] += 1
        j = i - 1
        lines_dict[5] += 1
        while j >= 0 and key < arr[j]:
            lines_dict[6] += 1
            arr[j + 1] = arr[j]
            lines_dict[7] += 1
            j -= 1
        lines_dict[8] += 1
        arr[j + 1] = key

    lines_dict[10] += 1
    return arr


