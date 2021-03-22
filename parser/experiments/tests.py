import random
import re
import dis, types
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

def checkIndent(string):
    index = 0
    while index < len(string) and string[index] == ' ':
        index += 1
    return index

def addInits(keyList):
    inits = ''
    # for x in range(varNum):
    #     inits += ("line" + str(x) + " = 0\n")
    inits += "lines_dict = {n : 0 for n in " + str(keyList) + "}\n"
    # inits += "lines_list = [0 for x in range(" + str(varNum) + ")]\n"
    return inits

def addLineVars(code):
    output = ""
    lineNum = 1
    keysList = []
    output += code.split('\n')[0] + '\n'
    for line in code.split('\n')[1:]:
        lineNum += 1

        spaceNum = checkIndent(line)
        if re.match(r'\s*#', line) != None or re.fullmatch(r'\s*', line):
            output += (line + '\n')
            continue
        elif re.match(r'\s*except ', line) != None:
            output += (line + '\n')
            output += (''.join([" " for _ in range(spaceNum + 4)]) + "lines_dict[" + str(lineNum) + "] += 1\n")
            keysList.append(lineNum)
        elif re.match(r' *else:', line) != None:
            output += (line + '\n')
        else:
            output += (''.join([" " for _ in range(spaceNum)]) + "lines_dict[" + str(lineNum) + "] += 1\n")
            output += (line + '\n')
            keysList.append(lineNum)

    output = addInits(keysList) + output
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

def saveAlgoToFile(algo):
    with open("parser/codeExamplesEdited/test_file_edited.py", 'w') as f:
        for line in algo.split("\n"):
            f.write(line + "\n")


def analyzeAlgoStack():
    # from codeExamples.mergeSort import mergeSort as ms
    from codeExamples.test_file import mergeSort as ms

    operations_dict = {}

    def analyzeCodeObject(codeObj, depth = 0):
        if depth < 0:
            return 

        # dis.dis(codeObj) # DEBUG
        it = dis.get_instructions(codeObj)

        line_index = -1
        for i in it:
            if type(i.argval) == types.CodeType: # If current instruction calls other code object, decent recursively
                analyzeCodeObject(i.argval, depth - 1)

            if i.starts_line is not None:
                operations_dict[i.starts_line] = []
                line_index = i.starts_line

            operations_dict[line_index].append(i.opcode)

    analyzeCodeObject(ms, 1) # Analyze code with depth 1
    return operations_dict




def countStackOperationsDict(lines_dict, op_dict):
    # if len(lines_dict) is not len(op_dict): 
    #     raise Exception("Wrong size of input lists")
    # print(lines_dict)
    operations_dict = {}
    for key in op_dict:
        # print(key)
        for op in op_dict[key]:
            if op not in operations_dict:
                operations_dict[op] = lines_dict[key]
            else:
                operations_dict[op] += lines_dict[key]

    return operations_dict





# Create python bytecode operations one the stack
operation_list = analyzeAlgoStack() 

# Read algo as a string

# algo = readAlgoFromFile()
from Parser import Parser
p = Parser()
fileFrom = "parser/codeExamples/test_file.py"
fileTo = "parser/codeExamplesEdited/test_file_edited.py"

p.parseCode(fileFrom, fileTo)

# saveAlgoToFile(algo_parsed)



# Edit it by adding line counts and save to the file
# saveEditedAlgoToFile(algo)

# Import edited merge as a function and run it

# from codeExamplesEdited.mergeSortEdited import mergeSort, lines_list
from codeExamplesEdited.test_file_edited import mergeSort, lines_dict

array = [random.randint(-1000, 1000) for _ in range(100)]

mergeSort(array)

# Generate dictionary of execution numbers for each stack operation
dictionary = countStackOperationsDict(lines_dict, operation_list)
print(lines_dict)
print(operation_list)
for key in dictionary.keys():
    print(dictionary[key], dis.opname[key], "code:", key)

# import py_compile
# print(py_compile.compile("./parser/tests.py"))
