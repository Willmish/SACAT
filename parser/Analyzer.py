import random
import dis, types
import importlib.util
from Settings import DEBUG

class Analyzer:
    def __init__(self):
        self.__operations_table = {} # Key - line number. Value - list of op codes
        self.__lines_execution = {} # Key - line number. Value - number of executions
        self.__operation_count = {} # Key - op code. Value - number of executions

        self.__unparsedModule = None
        self.__parsedModule = None

    
    @property
    def operations_table(self):
        return self.__operations_table

    def generate_operations_table(self, fileFrom):
        self.__unparsedModule = self.__importModule(fileFrom)
        self.__analyzeAlgoStack()

    @staticmethod
    def __importModule(filepath):
        spec = importlib.util.spec_from_file_location(filepath, filepath)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def initModules(self, fileUnparsed, fileParsed):
            self.__unparsedModule = self.__importModule(fileUnparsed)
            self.__parsedModule = self.__importModule(fileParsed)

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
                self.__operations_table[i.starts_line] = []
                line_index = i.starts_line

            if line_index == -1:
                raise Exception("Stack instructions analysis exception.\
                     Instruction set does not start with a line number.")

            self.__operations_table[line_index].append(i.opcode)

    def countStackOperations(self):
        self.__operation_count = {}
        for key in self.__operations_table:
            for opcode in self.__operations_table[key]:
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

    def analyze(self):
        self.countStackOperations()

    def test_analyze(self, filePaths):
        try:
            self.initModules(filePaths)
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




