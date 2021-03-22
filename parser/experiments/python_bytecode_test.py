
# expression = "[x for x in range(4)]"
# code = ast.parse(expression, mode='exec')
# # print(type(code))
# print(ast.dump(code, indent = 4))
# print(eval(compile(code, 'ast_test.py', mode='eval')))

# print(py_compile.compile("test.py"))

import dis
from types import CodeType

def a(x, y):
    for _ in range(10):
        a = 1
    return x + y
    
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

a = "\
def mul(x, y):\n\
    a = 23\n\
    b = 123\n\
    L = [1,2,3,4,5,6,7]\n\
    abc = [x for x in range(len(L))]\n\
    return a + 1\n\
"

def mul(x, y):
    a = [1,2,3]
    def abc():
        print(1)
    abc()
    return a


it = dis.get_instructions(mul)

dis.dis(mul)
# for i in it:
#     print(i)


import types 
print("LOL")
for i in it:
    if type(i.argval) == types.CodeType:
        dis.dis(i.argval)
        it = dis.get_instructions(i.argval)
        for i in it:
            print(i)
# operations_list = []

# line_index = -1
# for i in it:
#     if i.starts_line is not None:
#         operations_list.append([])
#         line_index += 1
#     operations_list[line_index].append(i.opcode)


# for i in range(len(operations_list)):
#     print(i, operations_list[i])

