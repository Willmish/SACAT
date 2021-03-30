from PyQt5.QtCore import pyqtSlot, QRunnable, QObject, pyqtSignal
import time
from src.testcontroller.test_controller import TestingController

# https://www.learnpyqt.com/tutorials/multithreading-pyqt-applications-qthreadpool/
class WorkerSignals(QObject):
    finished = pyqtSignal()
    result = pyqtSignal(object)
    error = pyqtSignal(object)

class TestingControllerWorker(QRunnable):
    """
    Worker "thread"

    :param kwargs: ??? t_max, T_max, time_analysis_bool etc., user.code
    """

    def __init__(self, user_code, parametersTuple, *args, **kwargs):
        super(TestingControllerWorker, self).__init__()
        self.args = args
        self.kwargs = kwargs
        self.user_code = user_code
        self.parametersTuple = parametersTuple
        self.user_code_path = None
        self.user_code_edited_path = None
        self.saveUserCode()
        self.signals = WorkerSignals()
        self.testing_controller = TestingController(self.user_code_path, self.user_code_edited_path, self.parametersTuple)


    def saveUserCode(self):
        # IMPORTANT that this stays in sacat_project/src/gui/
        # first gets the path of 2 directories above (sacat_project) and appends (seperator)input(seperator)filename.py
        from os.path import dirname, realpath, sep
        sacat_project_path = dirname(dirname(dirname(realpath(__file__))))
        self.user_code_path = sacat_project_path + sep + "res" + sep + "input" + sep + "mySort.py"
        self.user_code_edited_path = sacat_project_path + sep + "res" + sep + "input" + sep + "mySort_edited.py"
        with open(self.user_code_path, "w+") as f:
            f.write(self.user_code)


    @pyqtSlot()
    def run(self):
        try:
            self.testing_controller.run_full()
            # Long Computation
            result = 100
        except Exception as e:
            print(e)
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()
        # Run the necessary testing and store it