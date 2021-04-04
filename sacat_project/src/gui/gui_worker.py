from PyQt5.QtCore import pyqtSlot, QRunnable, QObject, pyqtSignal, QThread
import time, os
from src.testcontroller.test_controller import TestingController
from src.data_analysis.data_analyser import DataAnalyser
from multiprocessing import Process, Pipe, Queue
from src.data_analysis.results_storage import ResultsStorage


# https://www.learnpyqt.com/tutorials/multithreading-pyqt-applications-qthreadpool/
class WorkerSignals(QObject):
    finished = pyqtSignal(object)
    result = pyqtSignal(object)
    error = pyqtSignal(object)
    progress = pyqtSignal(tuple)

class TestingControllerWorker(QThread):
    """
    Worker "thread"

    :param kwargs: ??? t_max, T_max, time_analysis_bool etc., user.code
    """

    def __init__(self, user_code, parametersTuple, signals, pipe, *args, **kwargs):
        super(TestingControllerWorker, self).__init__()
        self.args = args
        self.kwargs = kwargs
        self.user_code = user_code
        self.parametersTuple = parametersTuple
        self.pipe = pipe
        self.signals = signals
        # TODO may need to capture in try-catch block
        self.process = None
        self.timeoutL = parametersTuple[10]
        self.startTime = None

    def startTimer(self):
        self.startTime = time.time()

    def endTimer(self):
        return time.time() - self.startTime

    def stopProcess(self):
        if self.process is not None:
            self.process.deleteFiles()
            self.process.terminate()
            self.process.kill()
            self.process = None

    @pyqtSlot()
    def run(self):
        self.startTimer()

        self.process = ProcessTest(self.user_code, self.parametersTuple, self.pipe)
        self.process.start()
        self.process.join(timeout=self.timeoutL)

        if self.process is not None:
            if self.process.is_alive():
                self.stopProcess()
                self.signals.error.emit("The time limit has been reached!")

        self.process = None
        self.signals.finished.emit(self.endTimer())


class ReceiverEmitter(QThread):
    def __init__(self, signals, pipe):
        super(ReceiverEmitter, self).__init__()
        self.signals = signals
        self.pipe = pipe
        self.running = True

    @pyqtSlot()
    def run(self):
        while self.running:
            packet = None
            try:
                packet = self.pipe.recv()
            except EOFError as e:
                # print(e)
                break

            if packet == 0:
                break
            if packet is not None:
                self.sendSignal(packet)

    def sendSignal(self, packet):
        (packet_type, packet_val) = packet
        if packet_type == 0:
            self.signals.progress.emit(packet_val)
        elif packet_type == 1:
            self.signals.result.emit(packet_val)
        elif packet_type == 2:
            self.signals.error.emit(packet_val)

    def stop(self):
        self.running = False

class ProcessTest(Process):
    def __init__(self, user_code, parametersTuple, pipe):
        super(ProcessTest, self).__init__()
        self.pipe = pipe
        self.user_code = user_code
        self.parametersTuple = parametersTuple
        self.user_code_path = "../../res/input/.mySort.py"
        self.user_code_edited_path = "../../res/input/.mySort_edited.py"
        self.saveUserCode()
        # TODO may need to capture in try-catch block
        self.testing_controller = TestingController(self.user_code_path, self.user_code_edited_path, self.parametersTuple)
        self.data_analyser = None

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

    def run(self):
        try:
            self.pipe.send((0, (10, "Testing code started...")))
            tested_data = self.testing_controller.run_full(self.pipe)
            self.pipe.send((0, (80, "Testing code finished...")))
            # time.sleep(1)
            self.pipe.send((0, (85, "Analyzing data...")))

            self.data_analyser = DataAnalyser(tested_data)
            results = self.data_analyser.full_data_analysis()
            self.pipe.send((0, (90, "Fetching results...")))

        except Exception as e:
            self.pipe.send((2, e))
        else:
            self.pipe.send((1, results))
        finally:
            self.deleteFiles()
            self.pipe.send((0, (100, "Finished")))
            self.pipe.send(0)  # Kill packet
