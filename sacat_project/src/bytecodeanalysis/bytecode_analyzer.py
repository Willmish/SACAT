import dis
import types

from src.settings import DEBUG


class BytecodeAnalyzer:
    def __init__(self, unparsedModule):
        self.__operations_table = {}  # Key - line number. Value - list of op codes
        self.__unparsedModule = unparsedModule

    @property
    def operations_table(self):
        return self.__operations_table

    def generate_operations_table(self):
        self.__analyzeCodeObject(self.__unparsedModule.mySort, 1)  # Analyze code with depth 1

    def __analyzeCodeObject(self, codeObj, depth=0):
        if depth < 0:
            return

        if DEBUG:
            dis.dis(codeObj)

        it = dis.get_instructions(codeObj)

        line_index = -1
        for i in it:
            if type(i.argval) == types.CodeType:  # If current instruction calls other code object, decent recursively
                self.__analyzeCodeObject(i.argval, depth - 1)

            if i.starts_line is not None:
                self.__operations_table[i.starts_line] = []
                line_index = i.starts_line

            if line_index == -1:
                raise Exception("Stack instructions analysis exception.\
                     Instruction set does not start with a line number.")

            self.__operations_table[line_index].append(i.opcode)
