from PyQt5.QtCore import pyqtSlot, QRunnable, QObject, pyqtSignal
import time

# https://www.learnpyqt.com/tutorials/multithreading-pyqt-applications-qthreadpool/
class WorkerSignals(QObject):
    finished = pyqtSignal()
    result = pyqtSignal(object)

class TestingControllerWorker(QRunnable):
    """
    Worker "thread"

    :param kwargs: ??? t_max, T_max, time_analysis_bool etc., user.code
    """

    def __init__(self, *args, **kwargs):
        super(TestingControllerWorker, self).__init__()
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            print(self.kwargs)
            # Long Computation
            time.sleep(5)
            result = 100
        except Exception as e:
            print(e)
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()
        # Run the necessary testing and store it