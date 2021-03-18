import random
import re

bubbleString = "\
def sort(arr):\n\
    for i in range(len(arr) - 1):\n\
        for j in range(0, len(arr) - i - 1):\n\
            if arr[j] > arr[j+1] :\n\
                arr[j], arr[j+1] = arr[j+1], arr[j]\n\
    return arr\n\
sort(array)"


quickSort = "\
def partition(arr, low, high):\n\
    i = (low-1)\n\
    pivot = arr[high]\n\
    for j in range(low, high):\n\
        if arr[j] <= pivot:\n\
            i = i+1\n\
            arr[i], arr[j] = arr[j], arr[i]\n\
    arr[i+1], arr[high] = arr[high], arr[i+1]\n\
    return (i+1)\n\
def quickSort(arr, low, high):\n\
    if len(arr) == 1:\n\
        return arr\n\
    if low < high:\n\
        pi = partition(arr, low, high)\n\
        quickSort(arr, low, pi-1)\n\
        quickSort(arr, pi+1, high)\n\
    return arr\n\
quickSort(array, 0, len(array) - 1)"


mergeSort = "\
def mergeSort(arr):\n\
    if len(arr) > 1:\n\
        mid = len(arr)//2\n\
        L = arr[:mid]\n\
        R = arr[mid:]\n\
        mergeSort(L)\n\
        mergeSort(R)\n\
        i = j = k = 0\n\
        while i < len(L) and j < len(R):\n\
            if L[i] < R[j]:\n\
                arr[k] = L[i]\n\
                i += 1\n\
            else:\n\
                arr[k] = R[j]\n\
                j += 1\n\
            k += 1\n\
        while i < len(L):\n\
            arr[k] = L[i]\n\
            i += 1\n\
            k += 1\n\
        while j < len(R):\n\
            arr[k] = R[j]\n\
            j += 1\n\
            k += 1\n\
    return arr\n\
mergeSort(array)"


def addGlobals(varNum, string):
    output = ''
    for line in string.split('\n'):
        output += line + "\n"
        if re.match(r' *def ', line) != None:
            spaceNum = checkIndent(line)
            for x in range(varNum):
                output += (''.join([" " for _ in range(spaceNum + 4)]) + "global line" + str(x)+ "\n")
    return output




def checkIndent(string):
    index = 0
    num = 0
    while string[index] == ' ':
        index += 1
        num += 1

    return num

def addFileSave(varNum):
    output = 'with open("log.txt", "w") as f:\n'
    for index in range(varNum):
        output += "    f.write(str(line" + str(index) + ")+ '\\n')\n"
        # output += "    f.write('\\n')\n"

    return output


def addInits(varNum):
    inits = ''
    for x in range(varNum):
        inits += ("line" + str(x) + " = 0\n")

    return inits

def addEndings(varNum):
    endings = ''
    for x in range(varNum):
        endings += ("print(" +'"line'+str(x)+' =",' + "line" + str(x) + ")" + "\n")
    
    return endings
        

def addLineVars(code):
    output = ""
    i = 0
    for line in code.split('\n'):
        spaceNum = checkIndent(line)
        if re.match(r' *else:', line) == None:
            output += (''.join([" " for _ in range(spaceNum)]) + "line" + str(i) + " += 1\n")
            i += 1

        output += (line + '\n')

    output = addInits(i) + output
    output += addEndings(i)
    output += addFileSave(i)
    output = addGlobals(i, output)
    return output



# Firstly check if your code has been edited properly | change quickSort into your code string

# print(addLineVars(quickSort))

# Sorting algorithm must be a function, which takes one parameter (list of numbers to sort)
# and at the end the algorithm must be run with parameter "array" - see examples above ^^^

# You can insert in your code 'print(array)' to visually check if its sorted

exec(addLineVars(bubbleString), {'array': [random.randint(-1000, 1000) for _ in range(1000)]}) 





