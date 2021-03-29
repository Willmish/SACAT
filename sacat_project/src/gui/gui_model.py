import random
import os.path
import time

# Other files
from gui_settings import settings
from gui_view import Ui_MainWindow

# External Libraries
from PyQt5 import QtCore,  QtWidgets
from PyQt5.QtWidgets import QMessageBox, QDockWidget, QMdiArea, QMdiSubWindow
from PyQt5.QtCore import pyqtSlot, Qt, QRunnable, QThreadPool, QObject, pyqtSignal

# Matplotlib
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from matplotlib.figure import Figure
from gui_worker import TestingControllerWorker

DOCKEXPERIMENT = False
MDIEXPERIMENT = False

# MATPLOTLIB WIDGET
# Reference: https://pyshine.com/How-to-make-a-GUI-using-PyQt5-and-Matplotlib-to-plot-real-....
class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)
        fig.tight_layout()

# Main Class
class SacatApp(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):

        # Calling GUI from GUI file
        super().__init__(*args, **kwargs)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Configuration
        self._setDefaults()
        self._connectButtons()
        self._createMatplotlibCanvas()
        self.showMaximized()
        # self.setStyleSheet(CSS_STYLESHEET)
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

    def _connectButtons(self):
        # Connecting buttons
        self.ui.buttonOpen.clicked.connect(self.openFile)
        self.ui.buttonSave.clicked.connect(self.saveFile)
        self.ui.buttonCheck.clicked.connect(self.checkCode)
        self.ui.buttonAnalyse.clicked.connect(self.analyseCode)
        self.ui.buttonScore.clicked.connect(self.scoreCode)
        self.ui.buttonHelp.clicked.connect(self.displayHelp)

    def _createMatplotlibCanvas(self):
        # Create the matplotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.
        self.ui.widget.setParent(None)
        self.ui.widget_3.setParent(None)
        self.upperPlot = MplCanvas(self, width=5, height=5, dpi=100)
        self.lowerPlot = MplCanvas(self, width=5, height=5, dpi=100)
        self.ui.plot_layout.addWidget(NavigationToolbar2QT(self.upperPlot, self))
        self.ui.plot_layout.addWidget(self.upperPlot)
        self.ui.plot_layout.addWidget(NavigationToolbar2QT(self.lowerPlot, self))
        self.ui.plot_layout.addWidget(self.lowerPlot)

        # In development: optional changes to plot graphs display and layout
        # experiment
        if MDIEXPERIMENT:
            self.mdi = QMdiArea()
            self.mdi.setMaximumWidth(1000)
            self.ui.plot_layout.addWidget(self.mdi)
            sub1 = QMdiSubWindow()
            sub1.setWidget(self.upperPlot)
            sub1.setWindowTitle("First plot")

            sub2 = QMdiSubWindow()
            sub2.setWidget(self.lowerPlot)
            sub2.setWindowTitle("Second plot")
            self.mdi.addSubWindow(sub1)
            self.mdi.addSubWindow(sub2)

            self.mdi.show()
            #self.mdi.cascadeSubWindows()
            #self.mdi.tileSubWindows()

        # experiment
        if DOCKEXPERIMENT:
            self.dockwidget1 = QDockWidget('Dock1', self)
            self.dockwidget1.setAllowedAreas(Qt.RightDockWidgetArea | Qt.LeftDockWidgetArea)
            self.dockwidget1.setFeatures(QDockWidget.DockWidgetFloatable | QDockWidget.DockWidgetMovable)
            self.dockwidget1.setWidget(self.upperPlot)
            self.dockwidget1.setFloating(False)

            self.dockwidget2 = QDockWidget('Dock2', self)
            self.dockwidget2.setAllowedAreas(Qt.RightDockWidgetArea | Qt.LeftDockWidgetArea)
            self.dockwidget2.setFeatures(QDockWidget.DockWidgetFloatable | QDockWidget.DockWidgetMovable)
            self.dockwidget2.setWidget(self.lowerPlot)
            self.dockwidget2.setFloating(False)

            self.addDockWidget(Qt.RightDockWidgetArea, self.dockwidget1)
            self.addDockWidget(Qt.RightDockWidgetArea, self.dockwidget2)

    def _setUpTimer(self, interval):
        self.timer = QtCore.QTimer()
        self.timer.setInterval(interval)
        self.timer.timeout.connect(self.updatePlot)
        self.timer.start()

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

    def updateProgressBar(self, value, text):
        self.ui.progressBar.setVisible(True)
        if value < 100:
            self.ui.progressBar.setValue(value)
            self.ui.progressBar.setFormat(text)

    def updatePlot(self, plotObject, xdata, ydata):
        """plotObject is either self.upperPlot or self.lowerPlot for now"""
        plotObject.axes.plot(xdata, ydata, 'r')
        plotObject.draw()

    @pyqtSlot()
    def openFile(self):
        try:
            name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open code file", "", "*.py;")
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
            name, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", "yourcode.py", "Python Files (*.py)")
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
    def checkCode(self):
        pass

    @pyqtSlot()
    def analyseCode(self):
        # HERE IT ALL STARTS
        # block input elements
        self._changeInputState(False)
        # get user input
        userInput = dict()
        userInput["TIME_ANALYSIS"] = self.ui.timeCheckbox.isChecked()
        userInput["NUM_OF_OP_ANALYSIS"] = self.ui.timeCheckbox.isChecked()
        userInput["SPACE_ANALYSIS"] = self.ui.spaceCheckbox.isChecked()
        userInput["SMALL_T"] = self.ui.tmaxSDoubleSpin.value()
        userInput["LARGE_T"] = self.ui.tmaxLDoubleSpin.value()
        #print(userInput)
        # Is userCode needed in a str form, or is the package just importing an existing file
        # What if user types code, where is it saved as a input file?
        # Shall I get the file name?
        self.userCode = self.ui.codeEditor.toPlainText() # can get user code in string form
        # just as an indicator
        self.updateProgressBar(1, "Starting analysis")
        # create and connect the worker thread
        worker = TestingControllerWorker(userInput=userInput)
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        #worker.signals.progress.connect(self.progress_fn)
        self.threadpool.start(worker)

    @pyqtSlot()
    def scoreCode(self):
        pass

    @pyqtSlot()
    def displayHelp(self):
        pass

    def thread_complete(self):
        self._changeInputState(True)
        print("THREAD COMPLETE")

    def print_output(self, r):
        print(r)


# if __name__ == '__main__':
#     app = QtWidgets.QApplication([])
#     # app.setAttribute(QtCore.Qt.AA_Use96Dpi)
#     window = BioreactorApp()
#     window.show()
#     app.exec_()