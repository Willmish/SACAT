from PyQt5.QtCore import pyqtSlot, QRunnable, QObject, pyqtSignal
import time, os
from src.testcontroller.test_controller import TestingController
from src.data_analysis.data_analyser import DataAnalyser

# https://www.learnpyqt.com/tutorials/multithreading-pyqt-applications-qthreadpool/
class WorkerSignals(QObject):
    finished = pyqtSignal()
    result = pyqtSignal(object)
    error = pyqtSignal(object)
    progress = pyqtSignal(tuple)

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
        self.user_code_path = "../../res/input/.mySort.py"
        self.user_code_edited_path = "../../res/input/.mySort_edited.py"
        self.saveUserCode()
        self.signals = WorkerSignals()
        # TODO may need to capture in try-catch block
        self.testing_controller = TestingController(self.user_code_path, self.user_code_edited_path, self.parametersTuple)
        self.data_analyser = None
        self.signals.progress.emit((10, "Testing object created..."))

    def saveUserCode(self):
        with open(self.user_code_path, "w") as f:
            f.write(self.user_code)

    def deleteFiles(self):
        if os.path.isfile(self.user_code_path):
            try:
                os.remove(self.user_code_path)
            except OSError as e:
                print(e)

        if os.path.isfile(self.user_code_edited_path):
            try:
                os.remove(self.user_code_edited_path)
            except OSError as e:
                print(e)


    @pyqtSlot()
    def run(self):
        try:
            tested_data = self.testing_controller.run_full()
            self.signals.progress.emit((34, "Testing code finished..."))
            time.sleep(1)
            self.signals.progress.emit((40, "Analyzing data..."))
            self.data_analyser = DataAnalyser(tested_data)
            results = self.data_analyser.full_data_analysis()
            self.signals.progress.emit((90, "Fetching results..."))
            for r in results:
                print(r)
            # Long Computation
            #result = 100

        except Exception as e:
            print("ERROR")
            self.signals.error.emit(e)
        else:
            self.signals.result.emit(results)
        finally:
            self.deleteFiles()
            self.signals.progress.emit((100, "Finished"))
            time.sleep(1)
            self.signals.finished.emit()

        # Run the necessary testing and store it
