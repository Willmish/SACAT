import random
import dis, types
import importlib.util
from Settings import DEBUG

class Analyzer:
    def __init__(self):
        self.__stack_operations = {} # Key - line number. Value - list of op codes
        self.__lines_execution = {} # Key - line number. Value - number of executions
        self.__operation_count = {} # Key - op code. Value - number of executions

        self.__unparsedModule = None
        self.__parsedModule = None

    def __importModule(self, filename, path):
        spec = importlib.util.spec_from_file_location(filename, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def __initModules(self, filesPaths):
            self.__unparsedModule = self.__importModule(filesPaths[0], filesPaths[1])
            self.__parsedModule = self.__importModule(filesPaths[2], filesPaths[3])

    def __analyzeAlgoStack(self):
        self.__analyzeCodeObject(self.__unparsedModule.mySort, 1) # Analyze code with depth 1

    def __analyzeCodeObject(self, codeObj, depth = 0):
        if depth < 0:
            return 

        if DEBUG:
            dis.dis(codeObj)

        it = dis.get_instructions(codeObj)

        line_index = -1
        for i in it:
            if type(i.argval) == types.CodeType: # If current instruction calls other code object, decent recursively
                self.__analyzeCodeObject(i.argval, depth - 1)

            if i.starts_line is not None:
                self.__stack_operations[i.starts_line] = []
                line_index = i.starts_line

            if line_index == -1:
                raise Exception("Stack instructions analysis exception.\
                     Instruction set does not start with a line number.")

            self.__stack_operations[line_index].append(i.opcode)

    def countStackOperations(self):
        for key in self.__stack_operations:
            for opcode in self.__stack_operations[key]:
                if opcode not in self.__operation_count:
                    self.__operation_count[opcode] = self.__lines_execution[key]
                else:
                    self.__operation_count[opcode] += self.__lines_execution[key]

    def executeAlgorithm(self, array = None):
        if array is None:
            array = [random.randint(-1000, 1000) for _ in range(100)]  

        try:
            self.__parsedModule.mySort(array)      
            self.__lines_execution = self.__parsedModule.lines_dict
        except Exception as e:
            print("User algorithm error.", str(e))

    def analyze(self, filePaths):
        try:
            self.__initModules(filePaths)
            self.__analyzeAlgoStack()

            self.executeAlgorithm()
            self.countStackOperations()

        except SyntaxError as e:
            print("User algorithm syntax error.")
            print(e.args[1][1], "line,", e.args[1][2], "column")
            print(e.args[1][3])
        except ImportError as e:
            print("User algorithm module loading error:", str(e))
        except Exception as e:
            print("Other error:", str(e))           

    def showAnalysisResults(self):
        for k in {k: v for k, v in sorted(self.__operation_count.items(), key=lambda item: item[1], reverse=True)}:
                print(self.__operation_count[k], dis.opname[k], "code:", k)




