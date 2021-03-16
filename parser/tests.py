import random
import re
import dis
from types import TracebackType

def bubbleSort(arr):
    for i in range(len(arr) - 1):
        for j in range(0, len(arr) - i - 1):
            if arr[j] > arr[j+1] :
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

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
    while index < len(string) and string[index] == ' ':
        index += 1
        num += 1
    return num

def addFileSave(varNum):
    output = 'with open("log.txt", "a+") as f:\n'
    # for index in range(varNum):
        # output += "    f.write(str(line" + str(index) + ")+ '\\n')\n"
        
        # output += "    f.write('\\n')\n"
    # output += "    f.write(str(list) + '\\n')\n"
    output += "    f.write(str(len(array)) + ';')\n"
    output += "    f.write(str(sum(lines_list)) + '\\n')\n"
    


    return output


def addInits(varNum):
    inits = ''
    # for x in range(varNum):
    #     inits += ("line" + str(x) + " = 0\n")
    inits += "lines_list = [0 for x in range(" + str(varNum) + ")]\n"
    return inits

def addEndings(varNum):
    endings = ''
    # for x in range(varNum):
    #     endings += ("print(" +'"line'+str(x)+' =",' + "line" + str(x) + ")" + "\n")
    endings += "print(lines_list)\n"
    endings += "print('operations count:', sum(lines_list))\n"
    return endings
        

def addLineVars(code):
    output = ""
    i = 0
    output += code.split('\n')[0] + '\n'
    for line in code.split('\n')[1:]:
        spaceNum = checkIndent(line)
        if re.match(r' *#', line) != None or re.fullmatch(r'\s*', line):
            continue
        elif re.match(r' *except ', line) != None:
            output += (''.join([" " for _ in range(spaceNum + 4)]) + "lines_list[" + str(i) + "] += 1\n")
            i += 1
        elif re.match(r' *else:', line) == None:
            # output += (''.join([" " for _ in range(spaceNum)]) + "line" + str(i) + " += 1\n")
            output += (''.join([" " for _ in range(spaceNum)]) + "lines_list[" + str(i) + "] += 1\n")
            i += 1
        

        output += (line + '\n')

    output = addInits(i) + output
    # output += addEndings(i)
    # output += addFileSave(i)
    # output = addGlobals(i, output)
    return output






def readAlgoFromFile():
    algo = ""
    with open("parser/codeExamples/test_file.py", 'r') as f:
        for line in f.readlines():
            algo += line

    return algo
def saveEditedAlgoToFile(algo):
    with open("parser/codeExamplesEdited/test_file_edited.py", 'w') as f:
        for line in addLineVars(algo).split("\n"):
            f.write(line + "\n")


def analyzeAlgoStack():
    # from codeExamples.mergeSort import mergeSort as ms
    from codeExamples.test_file import mergeSort as ms

    dis.dis(ms)
    it = dis.get_instructions(ms)

    operations_list = []

    line_index = -1
    for i in it:
        if i.starts_line is not None:
            operations_list.append([])
            line_index += 1
        operations_list[line_index].append(i.opcode)


    # for i in range(len(operations_list)):
    #     print(i, operations_list[i])

    return operations_list




def countStackOperations(lines_list, op_list):
    if len(lines_list) is not len(op_list): 
        raise Exception("Wrong size of input lists")

    operations_dict = {}
    for i in range(len(lines_list)):
        for entry in op_list[i]:
            if entry not in operations_dict:
                operations_dict[entry] = lines_list[i]
            else:
                operations_dict[entry] += lines_list[i]

    return operations_dict



# Create python bytecode operations one the stack
operation_list = analyzeAlgoStack() 

# Read algo as a string
algo = readAlgoFromFile()

# Edit it by adding line counts and save to the file
saveEditedAlgoToFile(algo)

# Import edited merge as a function and run it

# from codeExamplesEdited.mergeSortEdited import mergeSort, lines_list
from codeExamplesEdited.test_file_edited import mergeSort, lines_list

array = [random.randint(-1000, 1000) for _ in range(100)]

mergeSort(array)


# Generate dictionary of execution numbers for each stack operation
dictionary = countStackOperations(lines_list, operation_list)

for key in dictionary.keys():
    print(dictionary[key], dis.opname[key], "code:", key)

