# Other files
from src.gui.gui_settings import settings
from src.gui.gui_view import Ui_MainWindow
from src.gui.gui_worker import TestingControllerWorker, ReceiverEmitter, WorkerSignals

# Python Standard Library
import os.path
import multiprocessing as mp

# PyQt5
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt, QThreadPool, QObject, pyqtSlot, pyqtSignal

# Matplotlib
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from matplotlib.figure import Figure

# Stylesheet
import qdarkgraystyle

# GRAPH WINDOW WIDGET
class Event(QObject):
    closeWidget = pyqtSignal()

class GraphWindow(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(GraphWindow, self).__init__(*args, **kwargs)
        self.signal = Event()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        if a0.Close:
            self.signal.closeWidget.emit()

# MATPLOTLIB WIDGET
# Reference: https://pyshine.com/How-to-make-a-GUI-using-PyQt5-and-Matplotlib-to-plot-real-....
class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi, constrained_layout=True)

        self.axes = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)
        self.color = settings.get("DEFAULT_PLOT_COLOR")

    def setColor(self, color):
        self.color = color


# Main Class
class SacatApp(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):

        # Calling GUI from GUI file
        super().__init__(*args, **kwargs)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.closeEvent = self.closeEvent

        # Internal result saver
        self.r = None

        # Configuration
        self._setDefaults()
        self._connectButtons()
        self._createMatplotlibCanvas()
        self.setStyleSheet(qdarkgraystyle.load_stylesheet_pyqt5())
        self.ui.codeEditor.setStyleSheet(f"background-color: rgb(255,255,255); color: rgb(0,0,0);font-size: 16px")

        # Threadpool for worker computations
        # self.threadpool = QThreadPool()
        self.worker = None
        self.receiver_emitter = None
        self.testNumber = 0
        # Show
        self.showMaximized()
        self.ui.codeEditor.appendPlainText("def mySort(arr):\n"
                                           "\t#Your code goes here\n"
                                           "\treturn arr")

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.stopAnalysis()

    def _setDefaults(self):
        self.ui.progressBar.setVisible(False)
        self.ui.label_2.setText("SACAT v." + settings.get("VERSION"))
        self.ui.testcountSpin.setMinimum(settings.get("TEST_COUNT_MIN"))
        self.ui.testcountSpin.setMaximum(settings.get("TEST_COUNT_MAX"))
        self.ui.testcountSpin.setSingleStep(settings.get("TEST_COUNT_STEP"))
        self.ui.testcountSpin.setValue(settings.get("TEST_COUNT_DEFAULT"))
        self.ui.stepSpin.setMinimum(settings.get("TEST_STEP_MIN"))
        self.ui.stepSpin.setMaximum(settings.get("TEST_STEP_MAX"))
        self.ui.stepSpin.setSingleStep(settings.get("TEST_STEP_STEP"))
        self.ui.stepSpin.setValue(settings.get("TEST_STEP_DEFAULT"))
        self.ui.tmaxLDoubleSpin.setMinimum(settings.get("T_LARGE_MIN"))
        self.ui.tmaxLDoubleSpin.setMaximum(settings.get("T_LARGE_MAX"))
        self.ui.tmaxLDoubleSpin.setValue(settings.get("T_LARGE_DEFAULT"))
        self.ui.tmaxLDoubleSpin.setSingleStep(settings.get("T_LARGE_STEP"))
        self.ui.buttonColor_1.setStyleSheet(f"background-color: {settings.get('DEFAULT_PLOT_COLOR')}")
        self.ui.buttonColor_2.setStyleSheet(f"background-color: {settings.get('DEFAULT_PLOT_COLOR')}")
        self.ui.buttonUpperGraph.setStyleSheet(f"background-color: white")
        self.ui.buttonLowerGraph.setStyleSheet(f"background-color: white")
        self.ui.buttonClear_1.setStyleSheet(f"background-color: white")
        self.ui.buttonClear_2.setStyleSheet(f"background-color: white")
        self.ui.comboBox_mode_1.clear()
        self.ui.comboBox_group_1.clear()
        self.ui.comboBox_mode_2.clear()
        self.ui.comboBox_group_2.clear()

    def _connectButtons(self):
        # Connecting buttons
        self.ui.buttonOpen.clicked.connect(self.openFile)
        self.ui.buttonSave.clicked.connect(self.saveFile)
        self.ui.buttonAnalyse.clicked.connect(self.analyseCode)
        self.ui.buttonStop.clicked.connect(self.stopAnalysis)
        self.ui.buttonHelp.clicked.connect(self.showHelp)
        self.ui.buttonAdd_1.clicked.connect(self.managePlot)
        self.ui.buttonAdd_2.clicked.connect(self.managePlot)
        self.ui.buttonClear_1.clicked.connect(lambda: self.clearPlot(self.upperPlot))
        self.ui.buttonClear_2.clicked.connect(lambda: self.clearPlot(self.lowerPlot))
        self.ui.buttonColor_1.clicked.connect(lambda: self.pickPlotColor(self.upperPlot))
        self.ui.buttonColor_2.clicked.connect(lambda: self.pickPlotColor(self.lowerPlot))
        self.ui.buttonUpperGraph.clicked.connect(self.manageUpperGraphWindow)
        self.ui.buttonLowerGraph.clicked.connect(self.manageLowerGraphWindow)
        self.ui.radioButton.toggled.connect(lambda: self.allowTimeLimit(True))
        self.ui.radioButton_2.toggled.connect(lambda: self.allowTimeLimit(False))

    def _createMatplotlibCanvas(self):
        """
        Create the matplotlib FigureCanvas object
        which defines a single set of axes as self.axes
        """
        self.upperPlot = MplCanvas(self, width=5, height=5, dpi=100)
        self.lowerPlot = MplCanvas(self, width=5, height=5, dpi=100)
        self.upperNavToolbar = NavigationToolbar2QT(self.upperPlot, self)
        self.lowerNavToolbar = NavigationToolbar2QT(self.lowerPlot, self)
        self.upperNavToolbar.setStyleSheet("QToolButton { background-color: #ffffff; }")
        self.lowerNavToolbar.setStyleSheet("QToolButton { background-color: #ffffff; }")
        self.ui.plotLayoutUpper.addWidget(self.upperNavToolbar)
        self.ui.plotLayoutUpper.addWidget(self.upperPlot)
        self.ui.plotLayoutLower.addWidget(self.lowerNavToolbar)
        self.ui.plotLayoutLower.addWidget(self.lowerPlot)

    def _changeInputState(self, activate: bool):
        """All the input elements get blocked or unblocked depending on activate"""
        self.ui.buttonOpen.setEnabled(activate)
        self.ui.buttonSave.setEnabled(activate)
        self.ui.buttonAnalyse.setEnabled(activate)
        self.ui.timeCheckbox.setEnabled(activate)
        self.ui.numOfOpCheckbox.setEnabled(activate)
        self.ui.spaceCheckbox.setEnabled(activate)
        self.ui.label_6.setEnabled(activate)
        self.ui.testcountSpin.setEnabled(activate)
        self.ui.label_7.setEnabled(activate)
        self.ui.stepSpin.setEnabled(activate)
        self.ui.randomCheckbox.setEnabled(activate)
        self.ui.duplicatesCheckbox.setEnabled(activate)
        self.ui.sortedCheckbox.setEnabled(activate)
        self.ui.reversedCheckbox.setEnabled(activate)
        self.ui.tmaxLLabel.setEnabled(activate)
        self.ui.tmaxLDoubleSpin.setEnabled(activate)
        self.ui.codeEditor.setEnabled(activate)
        self.ui.comboBox_mode_1.setEnabled(activate)
        self.ui.comboBox_mode_2.setEnabled(activate)
        self.ui.comboBox_group_1.setEnabled(activate)
        self.ui.comboBox_group_2.setEnabled(activate)
        self.ui.buttonAdd_1.setEnabled(activate)
        self.ui.buttonAdd_2.setEnabled(activate)
        self.ui.radioButton.setEnabled(activate)
        self.ui.radioButton_2.setEnabled(activate)
        if activate and self.ui.radioButton_2.isChecked():
            self.ui.tmaxLLabel.setEnabled(False)
            self.ui.tmaxLDoubleSpin.setEnabled(False)

    @pyqtSlot()
    def openFile(self):
        """Gets called when 'Open' button is clicked"""
        try:
            sacat_project_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
            name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open code file", sacat_project_path, "*.py")
            if name != "":
                f = open(name, 'r')
                data = f.read()
                f.close()
                self.ui.codeEditor.clear()
                self.ui.codeEditor.appendPlainText(data)
                self.ui.fileNameLabel.setText(os.path.basename(name))
        except Exception as e:
            raise (Exception(f"File could not be opened: {e}"))

    @pyqtSlot()
    def saveFile(self):
        """Gets called when 'Save' button is clicked"""
        try:
            data = self.ui.codeEditor.toPlainText()
            sacat_project_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
            name, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save File",
                                                            sacat_project_path + os.path.sep + "yourcode.py",
                                                            "Python Files (*.py)")
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
        self.testNumber += 1
        self.ui.infoTextEdit.appendPlainText(f"RUN {self.testNumber}\n")
        self.r = None
        """Gets called when 'Analyse' button is clicked"""
        # Check if user input is valid
        if not(self.isValidUserInput()):
            return
        # Start progressbar
        self.ui.progressBar.setVisible(True)
        self.updateProgressBar((1, "Starting..."))
        # Block input elements
        self._changeInputState(False)
        # Graph Tab
        self.configureGraphTab()
        # Get user input
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
                           self.ui.radioButton_2.isChecked(),
                           self.ui.tmaxLDoubleSpin.value(),)

        # Create and connect the worker thread
        mother_pipe, child_pipe = mp.Pipe()
        self.signals = WorkerSignals()
        self.assignSignals()

        self.worker = TestingControllerWorker(user_code, parametersTuple, self.signals, child_pipe)
        self.receiver_emitter = ReceiverEmitter(self.signals, mother_pipe)

        self.ui.buttonStop.setEnabled(True)

        self.receiver_emitter.start()
        self.worker.start()


    @pyqtSlot()
    def stopAnalysis(self):
        # self.ui.plainTextEdit_2.clear()

        if self.worker is not None:
            self.worker.stopProcess()
        if self.receiver_emitter is not None:
            self.receiver_emitter.stop()

    @pyqtSlot()
    def displayHelp(self):
        pass

    def updateProgressBar(self, valueAndText):
        self.ui.progressBar.setVisible(True)
        if valueAndText[0] < 100:
            self.ui.progressBar.setValue(valueAndText[0])
            self.ui.progressBar.setFormat(valueAndText[1])


    def updatePlot(self, plotObject, xdata, ydata, group_name, y_pred=None):
        """plotObject is either self.upperPlot or self.lowerPlot for now"""
        plotObject.axes.scatter(xdata, ydata, color=plotObject.color, label=group_name)
        if y_pred is not None:
            plotObject.axes.plot(xdata, y_pred, color=plotObject.color)
        if plotObject.axes.get_legend() is not None:
            plotObject.axes.get_legend().remove()
        plotObject.axes.legend()
        plotObject.draw()

    def isValidUserInput(self):
        if not (self.isAtLeastOneAnalysisChecked()):
            self.showErrorMessage("NO OPTION CHOSEN",
                                  "You MUST choose at least one of the three given \n"
                                  "methods in \"Analyses\" Groupbox")
            return False

        if not (self.isAtLeastOneTestGroupChecked()):
            self.showErrorMessage("NO TESTGROUP CHOSEN",
                                  "You MUST choose at least one of the four given \n"
                                  "test groups in \"Testing\" Groupbox")
            return False
        return True

    def isAtLeastOneAnalysisChecked(self) -> bool:
        return self.ui.timeCheckbox.isChecked() or self.ui.numOfOpCheckbox.isChecked() or self.ui.spaceCheckbox.isChecked()

    def isAtLeastOneTestGroupChecked(self) -> bool:
        a = self.ui.randomCheckbox.isChecked() or self.ui.duplicatesCheckbox.isChecked()
        b = self.ui.sortedCheckbox.isChecked() or self.ui.reversedCheckbox.isChecked()
        return a or b

    def configureGraphTab(self):
        # Clear graphs and combo boxes
        self.upperPlot.axes.clear()
        self.lowerPlot.axes.clear()
        self.ui.comboBox_mode_1.clear()
        self.ui.comboBox_mode_2.clear()
        # Add options to combo boxes based on user input
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

    def assignSignals(self):
        self.signals.result.connect(self.saveAndDisplayResults)
        self.signals.finished.connect(self.threadComplete)
        self.signals.error.connect(self.showError)
        self.signals.progress.connect(self.updateProgressBar)

    def threadComplete(self, runningTime):
        self._changeInputState(True)
        self.updateProgressBar((0, ""))
        self.ui.progressBar.setVisible(False)
        self.ui.buttonStop.setEnabled(False)
        #print(runningTime)
        self.ui.logsTextEdit.appendPlainText(f"RUN {self.testNumber}\n")
        self.ui.logsTextEdit.appendPlainText("Running time: " + "{:.2f}".format(runningTime))
        if self.r is None:
            self.ui.infoTextEdit.appendPlainText("No output :(")
            self.ui.infoTextEdit.appendPlainText("-----------------------------------------------\n")
            self.ui.logsTextEdit.appendPlainText("Test unsuccessful.")
        else:
            self.ui.logsTextEdit.appendPlainText("Test successful.")

        self.ui.logsTextEdit.appendPlainText("-----------------------------------------------\n")
        # print("THREAD COMPLETE")

    def saveAndDisplayResults(self, r):
        """r is a Result-class object"""
        # Save last results, overwrite if necessary
        self.r = r
        # Display information
        self.show_info()
        # Manage graphs
        self.managePlot()
        self.receiver_emitter.stop()

    def show_info(self):
        if self.r is not None:
            # self.ui.infoTextEdit.clear()
            info = ""
            for res in self.r:
                if res is not None:
                    info += f"Test type: {res.test_type} \n"
                    if res.times_results is not None:
                        info += f"Time complexity based on time: {res.times_results[0]} \n"
                    if res.operations_results is not None:
                        info += f"Time complexity based on operations: {res.operations_results[0]} \n"
                    info += f"Most common operation: {res.most_common_operation} \n"
                    if res.space_results is not None:
                        info += f"Space complexity: {res.space_results[0]} \n"
            self.ui.infoTextEdit.appendPlainText(info)
            self.ui.infoTextEdit.appendPlainText("-----------------------------------------------\n")

    def managePlot(self):
        """
        Plots the results according to the sender:
            buttonAdd_1 : change upperPlot
            buttonAdd_2 : change lowerPlot
            ""          : means calling from analyseCode, change both plots
        """
        # Check if results exist
        if self.r is None:
            self.showErrorMessage("ERROR: NO DATA", "No results exist, click 'Analyse' to get results")
            return
        # Get the sender: buttonAdd_1 or buttonAdd_2 or ""
        sender = self.sender().objectName()

        # Default plots after Analyse
        if sender == "":
            # if more than 1 mode available, set second graph mode to the next possible one
            if self.ui.comboBox_mode_2.count() > 1:
                self.ui.comboBox_mode_2.setCurrentIndex(self.ui.comboBox_mode_1.currentIndex()+1)
            # if 1 mode available and more than 1 group, set second graph group to the next possible one
            elif self.ui.comboBox_mode_2.count() == 1 and self.ui.comboBox_group_2.count() > 1:
                self.ui.comboBox_group_2.setCurrentIndex(self.ui.comboBox_group_1.currentIndex()+1)

        # Get User Graph Settings
        groups = ["random", "duplicates", "sorted", "reversed"]
        graph_1_mode = self.ui.comboBox_mode_1.currentText()
        graph_2_mode = self.ui.comboBox_mode_2.currentText()
        group_1_text = self.ui.comboBox_group_1.currentText()
        group_2_text = self.ui.comboBox_group_2.currentText()
        graph_1_group = self.r[groups.index(group_1_text)]
        graph_2_group = self.r[groups.index(group_2_text)]
        fit_1 = self.ui.checkBoxFit_1.isChecked()
        fit_2 = self.ui.checkBoxFit_2.isChecked()
        # Change plot
        if sender == "buttonAdd_1" or sender == "":  # upperPlot
            self.changePlot(graph_1_group, graph_1_mode, self.upperPlot, self.ui.comboBox_group_1.currentText(),
                            fit=fit_1)
        if sender == "buttonAdd_2" or sender == "":  # lowerPlot
            self.changePlot(graph_2_group, graph_2_mode, self.lowerPlot, self.ui.comboBox_group_2.currentText(),
                            fit=fit_2)
        # If graph opened in seperate window, raise it
        try:
            if self.graphWindowUpper.isVisible() and (sender == "buttonAdd_1" or sender == ""):
                self.graphWindowUpper.raise_()
        except AttributeError:
            pass
        try:
            if self.graphWindowLower.isVisible() and (sender == "buttonAdd_2" or sender == ""):
                self.graphWindowLower.raise_()
        except AttributeError:
            pass

    def changePlot(self, group, mode, graph, group_name, fit):
        # Check mode
        if mode == "Time analysis":
            bestfit, coefs, y_pred, y, sizes = group.times_results
        elif mode == "Number of operations analysis":
            bestfit, coefs, y_pred, y, sizes = group.operations_results
        else:  # Space analysis
            bestfit, coefs, y_pred, y, sizes = group.space_results
        # Update plot
        if fit: # if fitted curve checked
            self.updatePlot(graph, sizes, y, group_name, y_pred)
        else:
            self.updatePlot(graph, sizes, y, group_name)

    def clearPlot(self, plotObject):
        """Clears plotObject: either upperPlot or lowerPlot"""
        plotObject.axes.clear()
        plotObject.draw()
        # If graph opened in seperate window, raise it
        try:
            if plotObject is self.upperPlot and self.graphWindowUpper.isVisible():
                self.graphWindowUpper.raise_()
            if plotObject is self.lowerPlot and self.graphWindowLower.isVisible():
                self.graphWindowLower.raise_()
        except AttributeError: # graphWindow doesn't exist, don't set focus
            pass

    def pickPlotColor(self, plotObject):
        """Color picker for a given plotObject"""
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self.sender().setStyleSheet(f"background-color: {color.name()}")
            plotObject.setColor(color.name())

    def manageUpperGraphWindow(self):
        if self.sender().isChecked():
            self.graphWindowUpper = GraphWindow()
            self.graphWindowUpper.setWindowTitle("Upper Graph")
            self.graphWindowUpper.resize(500, 400)
            self.graphWindowUpper.setMinimumSize(500, 400)
            self.newLayoutUpper = QtWidgets.QVBoxLayout()
            self.newLayoutUpper.addWidget(self.upperNavToolbar)
            self.newLayoutUpper.addWidget(self.upperPlot)
            self.graphWindowUpper.setLayout(self.newLayoutUpper)
            self.graphWindowUpper.signal.closeWidget.connect(lambda: self.putUpperPlotInApp(True))
            self.graphWindowUpper.show()
        else:
            self.graphWindowUpper.destroy()
            self.putUpperPlotInApp()

    def manageLowerGraphWindow(self):
        if self.sender().isChecked():
            self.graphWindowLower = GraphWindow()
            self.graphWindowLower.setWindowTitle("Lower Graph")
            self.graphWindowLower.resize(500, 400)
            self.graphWindowLower.setMinimumSize(500, 400)
            self.newLayoutLower = QtWidgets.QVBoxLayout()
            self.newLayoutLower.addWidget(self.lowerNavToolbar)
            self.newLayoutLower.addWidget(self.lowerPlot)
            self.graphWindowLower.setLayout(self.newLayoutLower)
            self.graphWindowLower.signal.closeWidget.connect(lambda: self.putLowerPlotInApp(True))
            self.graphWindowLower.show()
        else:
            self.graphWindowLower.destroy()
            self.putLowerPlotInApp()

    def putUpperPlotInApp(self, doToggle=False):
        if doToggle:
            self.ui.buttonUpperGraph.toggle()
        self.ui.plotLayoutUpper.addWidget(self.upperNavToolbar)
        self.upperPlot.resize(400, 500)
        self.ui.plotLayoutUpper.addWidget(self.upperPlot)

    def putLowerPlotInApp(self, doToggle=False):
        if doToggle:
            self.ui.buttonLowerGraph.toggle()
        self.ui.plotLayoutLower.addWidget(self.lowerNavToolbar)
        self.lowerPlot.resize(400, 500)
        self.ui.plotLayoutLower.addWidget(self.lowerPlot)

    def allowTimeLimit(self, bool):
        self.ui.tmaxLLabel.setEnabled(bool)
        self.ui.tmaxLDoubleSpin.setEnabled(bool)

    def showErrorMessage(self, title, text, information=None, details=None):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setWindowTitle(title)
        msg.setText(text)
        if information:
            msg.setInformativeText(information)
        if details:
            msg.setDetailedText(details)
        msg.exec_()

    def showError(self, s):
        self.showErrorMessage("ERROR", str(s))

    def showHelp(self):
        try:
            self.widget = QtWidgets.QWidget()
            self.widget.setMinimumSize(800, 800)
            #self.widget.setFixedSize(800, 700) # TODO: set fixed size when finished help text
            self.widget.setWindowTitle("Help")
            layout1 = QtWidgets.QHBoxLayout()
            layout1.setAlignment(Qt.AlignTop)
            layout1.setContentsMargins(20, 10, 20, 10)
            self.widget.setLayout(layout1)
            label = QtWidgets.QLabel()
            label.setTextInteractionFlags(Qt.TextBrowserInteraction)
            label.setOpenExternalLinks(True)
            label.setStyleSheet("QLabel {background-color: white;padding: 10px 30px 20px 30px;}")
            infoText = """
            <style>
              h1 {text-align: center}
              li, div {font-size:16px}
            </style>
            <h1> HELP </h1>
            <h2>Starting an analysis</h2>
            <ol>
                <li> Write your code in the text editor on the left, inside of a function called mySort which returns a sorted array. </li>
                <li> Select what types of Analysis you want to perform (Time complexity: based on time, based on no of operations, Space complexity) </li>
                <li> Choose number of tests per each test type, choose step (by how much the array increases in size). </li>
                <li> Choose which types of test to perform (Random (arrays with random integers), Duplicates (random integers in a small range), 
                Sorted (pre sorted arrays) and Reversed (arrays sorted in descending order).</li>
                <li> Choose upper time limit for the Analysis (or select none). (The program will automatically pause if time limit reached) </li>
                <li> Press Analyse at the top of the screen to begin the analysis. </li>
                <li> At any time you can press Stop to pause the execution of the program. </li>
            </ol>
            <h2>Viewing the results</h2>
            <ol>
                <li> You can use open and save buttons at the top of the screen to Open an existing python file 
                or save the current program (as a python file). </li>
                <li> Info section on the right: Contains output information from each run of the analysis. 
                (Time complexity achieved, Most common Operation, Space complexity estimated) </li>
                <li> Chart Section (on the right)
                <ol>
                    <li>There are 2 empty graphs which can be "popped out" using <img src="src/gui/graphics/maximize.ico" width="20" height="20"
                    alt="maximize"></li>
                    <li>The graphs can be cleared using <img src="src/gui/graphics/rubber.ico" width="20" height="20" alt="plus"> button 
                    and new graphs can be added with <img src="src/gui/graphics/plus.ico" width="20" height="20" alt="rubber"> button</li>
                    <li>For each graph to be added, select the type of analysis result, type of test, 
                    whether to show the fitted curve or not and the colour.</li>
                </ol>
            </ol>
            <h2> About </h2>
            <div>
            Icons made by <a href="https://icons8.com" title="Icons8">Icons8</a> and 
                          <a href="http://www.designcontest.com">DesignContest</a>
            </div>
            """
            label.setWordWrap(True)
            label.setText(infoText)
            layout1.addWidget(label)
            self.widget.show()
        except Exception as e:
            self.showErrorMessage("ERROR", str(e))