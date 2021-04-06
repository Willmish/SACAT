import importlib.util

from src.bytecodeanalysis.bytecode_analyzer import BytecodeAnalyzer
from src.parser.parser import Parser
from src.precheck.user_code import UserCode
from src.pretest.pre_tests import PreTest
from src.runenv.run_environment import RunEnvironment
from settings import *

class TestingController:
    def __init__(self, user_code_path, user_code_edited_path, parametersTuple):
        # (time_analysis: bool, numofop_analisys: bool, space_analysis: bool, testcount: int, step: int, random : bool,
        # duplicates: bool, sorted: bool, reversed: bool, tmax: int, Tmax: int)
        self.__unparsedModule = None
        self.__parsedModule = None
        self.__uc = None
        self.__op_table = None
        self.__user_code_path = user_code_path
        self.__user_code_edited_path = user_code_edited_path
        self.doTimeAnalysis, self.doNumOpAnalysis, self.doSpaceAnalysis, self.test_count, \
        self.step, self.random, self.duplicate, self.sortedd, self.reversedd, self.t_max, self.T_max = parametersTuple

    def loadUserCode(self):
        # TODO change fileFrom to a parameter passed from the GUI
        self.__uc = UserCode(self.__user_code_path)
        self.checkCode(self.__uc)
        self.__unparsedModule = self.__importModule(self.__user_code_path)  # Import user module

    @staticmethod
    def checkCode(uc):
        uc.checkForRestricted()

    def preTest(self):
        pre_test = PreTest(self.__unparsedModule)
        try:
            run_time, failed = pre_test.run()
        except Exception as e:
            raise Exception("User code exception: " + str(e))

        if len(failed) != 0:
            # print("Some tests failed!")  # TMP
            raise Exception("User code does not sort properly! Failed tests:" + str(failed))
            # return

    def parseCode(self):
        p = Parser()
        p.parseCode(self.__uc, self.__user_code_edited_path)

        ec = UserCode(self.__user_code_edited_path)
        self.checkCode(ec)  # Check if there was no malicious code added to the edited file
        self.__parsedModule = self.__importModule(self.__user_code_edited_path)  # Import parsed module

    def analyseBytecode(self):
        a = BytecodeAnalyzer(self.__unparsedModule)
        a.generate_operations_table()
        self.__op_table = a.operations_table

    def run_env(self, pipe):
        # TODO change step and max_tests number as parameters from the GUI
        re = RunEnvironment(self.__unparsedModule, self.__parsedModule, self.__op_table, t_max=self.t_max,
                            T_max=self.T_max, step=self.step, max_tests=self.test_count, pipe=pipe)

        results = re.run(self.doTimeAnalysis, self.doNumOpAnalysis, self.doSpaceAnalysis, random=self.random,
                         duplicate=self.duplicate, sortedd=self.sortedd, reversedd=self.reversedd)

        return results

    def run_full(self, pipe):
        self.loadUserCode()
        self.preTest()
        self.parseCode()
        self.analyseBytecode()
        return self.run_env(pipe)

    @staticmethod
    def __importModule(filepath):
        spec = importlib.util.spec_from_file_location(filepath, filepath)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
