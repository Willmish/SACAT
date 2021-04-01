import random
import os.path
import time

# Other files
from gui_settings import settings
from gui_14 import Ui_MainWindow

# External Libraries
from PyQt5 import QtCore,  QtWidgets, QtGui
from PyQt5.QtWidgets import QMessageBox, QDockWidget, QMdiArea, QMdiSubWindow
from PyQt5.QtCore import pyqtSlot, Qt, QRunnable, QThreadPool, QObject, pyqtSignal

# Matplotlib
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from matplotlib.figure import Figure
from gui_worker import TestingControllerWorker
import qdarkstyle
import qdarkgraystyle

# MATPLOTLIB WIDGET
# Reference: https://pyshine.com/How-to-make-a-GUI-using-PyQt5-and-Matplotlib-to-plot-real-....
class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi, constrained_layout=True)

        self.axes = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)
        self.color = "#00FF00"

    def setColor(self, color):
        self.color = color

# Main Class
class SacatApp(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):

        # Calling GUI from GUI file
        super().__init__(*args, **kwargs)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Internal result saver
        self.r = None

        # Configuration
        self._setDefaults()
        self._createMatplotlibCanvas()
        self._connectButtons()
        self.showMaximized()
        self.setStyleSheet(qdarkgraystyle.load_stylesheet_pyqt5())
        self.ui.codeEditor.setStyleSheet("background-color: rgb(255,255,255); color: rgb(0,0,0)")
        # Threadpool for worker computations
        self.threadpool = QThreadPool()

    def _setDefaults(self):
        self.ui.progressBar.setVisible(False)
        self.ui.label_2.setText("SACAT v." + settings.get("VERSION"))
        self.ui.tmaxSDoubleSpin.setMinimum(settings.get("T_SMALL_MIN"))
        self.ui.tmaxSDoubleSpin.setMaximum(settings.get("T_SMALL_MAX"))
        self.ui.tmaxSDoubleSpin.setValue(settings.get("T_SMALL_DEFAULT"))
        self.ui.tmaxLDoubleSpin.setSingleStep(0.5)
        self.ui.tmaxLDoubleSpin.setMinimum(settings.get("T_LARGE_MIN"))
        self.ui.tmaxLDoubleSpin.setMaximum(settings.get("T_LARGE_MAX"))
        self.ui.tmaxLDoubleSpin.setValue(settings.get("T_LARGE_DEFAULT"))
        self.ui.tmaxLDoubleSpin.setSingleStep(settings.get("T_LARGE_INC"))
        self.ui.comboBox_mode_1.clear()
        self.ui.comboBox_group_1.clear()
        self.ui.comboBox_mode_2.clear()
        self.ui.comboBox_group_2.clear()

    def _connectButtons(self):
        # Connecting buttons
        self.ui.buttonOpen.clicked.connect(self.openFile)
        self.ui.buttonSave.clicked.connect(self.saveFile)
        self.ui.buttonAnalyse.clicked.connect(self.analyseCode)
        self.ui.buttonHelp.clicked.connect(self.displayHelp)
        self.ui.buttonAdd_1.clicked.connect(self.managePlot1)
        self.ui.buttonAdd_2.clicked.connect(self.managePlot2)
        self.ui.buttonClear_1.clicked.connect(self.clearUpperPlot)
        self.ui.buttonClear_2.clicked.connect(self.clearLowerPlot)
        self.ui.buttonColor_1.clicked.connect(self.pickColor_1)
        self.ui.buttonColor_2.clicked.connect(self.pickColor_2)

    def _createMatplotlibCanvas(self):
        # Create the matplotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.
        self.upperPlot = MplCanvas(self, width=5, height=5, dpi=100)
        self.lowerPlot = MplCanvas(self, width=5, height=5, dpi=100)
        self.ui.plot_layout.addWidget(NavigationToolbar2QT(self.upperPlot, self))
        self.ui.plot_layout.addWidget(self.upperPlot)
        self.ui.plot_layout.addWidget(NavigationToolbar2QT(self.lowerPlot, self))
        self.ui.plot_layout.addWidget(self.lowerPlot)
        # self.upperPlot.axes.axis([0,10,0,10])
        # self.upperPlot.axes.text(4, 5, 'GRAPH 1', fontsize=32)
        # self.lowerPlot.axes.axis([0, 10, 0, 10])
        # self.lowerPlot.axes.text(4, 5, 'GRAPH 2', fontsize=32)

    def _changeInputState(self, activate:bool):
        """all the input elements get blocked or unblocked depending on activate"""
        self.ui.buttonOpen.setEnabled(activate)
        self.ui.buttonSave.setEnabled(activate)
        self.ui.buttonAnalyse.setEnabled(activate)
        self.ui.timeCheckbox.setEnabled(activate)
        self.ui.numOfOpCheckbox.setEnabled(activate)
        self.ui.spaceCheckbox.setEnabled(activate)
        self.ui.tmaxSDoubleSpin.setEnabled(activate)
        self.ui.tmaxLDoubleSpin.setEnabled(activate)
        self.ui.codeEditor.setEnabled(activate)

    def showErrorMessage(self, title, text, information=None, details=None):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle(title)
        msg.setText(text)
        if information:
            msg.setInformativeText(information)
        if details:
            msg.setDetailedText(details)
        msg.exec_()

    def updateProgressBar(self, valueAndText):
        self.ui.progressBar.setVisible(True)
        if valueAndText[0] < 100:
            self.ui.progressBar.setValue(valueAndText[0])
            self.ui.progressBar.setFormat(valueAndText[1])

    def updatePlot(self, plotObject, xdata, ydata):
        """plotObject is either self.upperPlot or self.lowerPlot for now"""
        # plotObject.axes.clear()
        plotObject.axes.scatter(xdata, ydata, color=plotObject.color)
        plotObject.draw()


    @pyqtSlot()
    def openFile(self):
        try:
            sacat_project_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
            name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open code file", sacat_project_path, "*.py")
            if name != "":
                f = open(name, 'r')
                data = f.read()
                f.close()
                self.ui.codeEditor.clear()
                self.ui.codeEditor.insertPlainText(data)
                self.ui.fileNameLabel.setText(os.path.basename(name))
        except Exception as e:
            raise(Exception(f"File could not be opened: {e}"))

    @pyqtSlot()
    def saveFile(self):
        try:
            data = self.ui.codeEditor.toPlainText()
            sacat_project_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
            name, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", sacat_project_path + os.path.sep + "yourcode.py", "Python Files (*.py)")
            if name:
                if name[-3:] != ".py":
                    file = open(name + ".py", 'w')
                else:
                    file = open(name, 'w')
                file.writelines(data)
                file.close()
                self.ui.fileNameLabel.setText(os.path.basename(name))
        except Exception as e:
            raise (Exception(f"File could not be saved: {e}"))

    @pyqtSlot()
    def analyseCode(self):
        # Checking for valid user settings
        if not(self.isAtLeastOneAnalysisChecked()):
            self.showErrorMessage("NO OPTION CHOSEN",
                                  "You MUST choose at least one of the three given \n"
                                  "methods in \"Analyses\" Groupbox")
            return

        if not(self.isAtLeastOneTestGroupChecked()):
            self.showErrorMessage("NO TESTGROUP CHOSEN",
                                  "You MUST choose at least one of the four given \n"
                                  "test groups in \"Testing\" Groupbox")
            return

        # Graph Tab
        self.upperPlot.axes.clear()
        self.lowerPlot.axes.clear()

        self.ui.comboBox_mode_1.clear()
        self.ui.comboBox_mode_2.clear()
        if self.ui.timeCheckbox.isChecked():
            self.ui.comboBox_mode_1.addItem("Time analysis")
            self.ui.comboBox_mode_2.addItem("Time analysis")
        if self.ui.numOfOpCheckbox.isChecked():
            self.ui.comboBox_mode_1.addItem("Number of operations analysis")
            self.ui.comboBox_mode_2.addItem("Number of operations analysis")
        if self.ui.spaceCheckbox.isChecked():
            self.ui.comboBox_mode_1.addItem("Space analysis")
            self.ui.comboBox_mode_2.addItem("Space analysis")
        self.ui.comboBox_group_1.clear()
        self.ui.comboBox_group_2.clear()
        if self.ui.randomCheckbox.isChecked():
            self.ui.comboBox_group_1.addItem("random")
            self.ui.comboBox_group_2.addItem("random")
        if self.ui.duplicatesCheckbox.isChecked():
            self.ui.comboBox_group_1.addItem("duplicates")
            self.ui.comboBox_group_2.addItem("duplicates")
        if self.ui.sortedCheckbox.isChecked():
            self.ui.comboBox_group_1.addItem("sorted")
            self.ui.comboBox_group_2.addItem("sorted")
        if self.ui.reversedCheckbox.isChecked():
            self.ui.comboBox_group_1.addItem("reversed")
            self.ui.comboBox_group_2.addItem("reversed")

        # Start
        self.updateProgressBar((1, "Starting...")) # just an indicator
        # block input elements
        self._changeInputState(False)
        # get user input
        user_code = self.ui.codeEditor.toPlainText()
        parametersTuple = (self.ui.timeCheckbox.isChecked(),
                           self.ui.numOfOpCheckbox.isChecked(),
                           self.ui.spaceCheckbox.isChecked(),
                           self.ui.testcountSpin.value(),
                           self.ui.stepSpin.value(),
                           self.ui.randomCheckbox.isChecked(),
                           self.ui.duplicatesCheckbox.isChecked(),
                           self.ui.sortedCheckbox.isChecked(),
                           self.ui.reversedCheckbox.isChecked(),
                           self.ui.tmaxSDoubleSpin.value(),
                           self.ui.tmaxLDoubleSpin.value(),)

        # create and connect the worker thread
        worker = TestingControllerWorker(user_code, parametersTuple)
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.error.connect(self.showError)
        worker.signals.progress.connect(self.updateProgressBar)
        #worker.signals.progress.connect(self.progress_fn)
        self.threadpool.start(worker)

    def isAtLeastOneAnalysisChecked(self):
        return self.ui.timeCheckbox.isChecked() or self.ui.numOfOpCheckbox.isChecked() or self.ui.spaceCheckbox.isChecked()

    def isAtLeastOneTestGroupChecked(self):
        a = self.ui.randomCheckbox.isChecked() or self.ui.duplicatesCheckbox.isChecked()
        b = self.ui.sortedCheckbox.isChecked() or self.ui.reversedCheckbox.isChecked()
        return a or b

    @pyqtSlot()
    def displayHelp(self):
        pass

    def thread_complete(self):
        self._changeInputState(True)
        self.updateProgressBar((0,""))
        self.ui.progressBar.setVisible(False)
        print("THREAD COMPLETE")

    def print_output(self, r):
        """r is a Result-class object"""
        # Save last results, overwrite if necessary
        self.r = r
        # Display information
        # for result in r:
        #     self.ui.plainTextEdit_2.insertPlainText(f"Test type {result.test_type}")
        #     self.ui.plainTextEdit_2.insertPlainText(f"Best  fit {result.times_results}")
        # [random, duplicates, sorted, reversed]
        # Manage graphs
        self.managePlots()
        #print(r)


    def managePlots(self, g1=True, g2=True):
        if self.r is None:
            self.showErrorMessage("ERROR: NO DATA", "No results data exist, run Analysis firstly")
            return
        groups = ["random", "duplicates", "sorted", "reversed"]
        # modes = ["Time analysis", "Number of operations analysis", "Space analysis"]
        graph_1_mode = self.ui.comboBox_mode_1.currentText()
        graph_2_mode = self.ui.comboBox_mode_2.currentText()
        graph_1_group = self.r[groups.index(self.ui.comboBox_group_1.currentText())]
        graph_2_group = self.r[groups.index(self.ui.comboBox_group_2.currentText())]
        if g1 == True:
            self.changePlot(graph_1_group, graph_1_mode, self.upperPlot) # graph 1
        if g2 == True:
            self.changePlot(graph_2_group, graph_2_mode, self.lowerPlot) # graph 2

    def managePlot1(self):
        self.managePlots(True, False)

    def managePlot2(self):
        self.managePlots(False, True)

    def changePlot(self, group, mode, graph):
        if mode == "Time analysis":
            bestfit, coefs, y_pred, y, sizes = group.times_results
        elif mode == "Number of operations analysis":
            bestfit, coefs, y_pred, y, sizes = group.operations_results
        else:  # Space analysis
            bestfit, coefs, y_pred, y, sizes = group.space_results
        self.updatePlot(graph, sizes, y)

    def clearUpperPlot(self):
        self.upperPlot.axes.clear()
        self.updatePlot(self.upperPlot, [], [])

    def clearLowerPlot(self):
        self.lowerPlot.axes.clear()
        self.updatePlot(self.lowerPlot, [], [])

    def pickColor_1(self):
        color = QtWidgets.QColorDialog.getColor()

        if color.isValid():
            self.ui.buttonColor_1.setStyleSheet(f"background-color: {color.name()}")
            #self.upperPlot.axes.set_facecolor("blue")
            self.upperPlot.setColor(color.name())

    def pickColor_2(self):
        color = QtWidgets.QColorDialog.getColor()

        if color.isValid():
            self.ui.buttonColor_2.setStyleSheet(f"background-color: {color.name()}")
            self.lowerPlot.setColor(color.name())
            #self.lowerPlot.axes.set_facecolor("blue")

    def showError(self, s):
        self.showErrorMessage("ERROR", str(s))


# if __name__ == '__main__':
#     app = QtWidgets.QApplication([])
#     # app.setAttribute(QtCore.Qt.AA_Use96Dpi)
#     window = BioreactorApp()
#     window.show()
#     app.exec_()