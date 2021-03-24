import importlib.util

from src.bytecodeanalysis.bytecode_analyzer import BytecodeAnalyzer
from src.parser.parser import Parser
from src.precheck.user_code import UserCode
from src.precheck.errors import RestrictedCodeError
from src.pretest.pre_tests import PreTest
from src.runenv.run_environment import RunEnvironment
from src.settings import *


class TestingController:
    def __init__(self):
        self.__unparsedModule = None
        self.__parsedModule = None
        self.__uc = None
        self.__op_table = None

    def checkUserCode(self):
        self.__uc = UserCode(fileFrom)
        try:
            self.__uc.checkForRestricted()
        except RestrictedCodeError as e:
            print(e.message, ':', e.restrictedElement)
            return

        self.__unparsedModule = self.__importModule(fileFrom)  # Import user module

    def preTest(self):
        pre_test = PreTest()
        run_time, failed = pre_test.run(self.__unparsedModule.mySort)
        print(run_time, failed)
        if len(failed) != 0:
            print("Some tests failed!")  # TMP
            # return

    def parseCode(self):
        p = Parser()
        p.parseCode(self.__uc, fileTo)

        self.__parsedModule = self.__importModule(fileTo)  # Import parsed module

    def analyseBytecode(self):
        a = BytecodeAnalyzer(self.__unparsedModule)
        a.generate_operations_table()
        self.__op_table = a.operations_table

    def run_env(self):
        re = RunEnvironment(self.__unparsedModule, self.__parsedModule, self.__op_table)
        results = re.run(True, True, False, True, True, True, True)
        for storage in results:
            print(storage)

    def run_full(self):
        self.checkUserCode()
        self.preTest()
        self.parseCode()
        self.analyseBytecode()
        self.run_env()

    @staticmethod
    def __importModule(filepath):
        spec = importlib.util.spec_from_file_location(filepath, filepath)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

tc = TestingController()
tc.run_full()
