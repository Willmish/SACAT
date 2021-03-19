import random

# Other files
from settings import *
from guis.gui_8 import Ui_MainWindow

# External Libraries
from PyQt5 import QtCore,  QtWidgets
from PyQt5.QtCore import pyqtSlot

# Matplotlib
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from matplotlib.figure import Figure

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

        # First configuration (SETTINGS)
        self.ui.label_2.setText("SACAT v." + settings.get('VERSION'))
        # self.ui.tmaxSDoubleSpin.setMinimum(settings.get("T_SMALL_MININUM"))
        # self.ui.tmaxSDoubleSpin.setMaximum(settings.get("T_SMALL_MAXIMUM"))
        # self.ui.tmaxSDoubleSpin.setValue(settings.get("T_SMALL_DEFAULT"))
        # self.ui.tmaxLDoubleSpin.setMinimum(settings.get("T_LARGE_MINIMUM"))
        # self.ui.tmaxLDoubleSpin.setMaximum(settings.get("T_LARGE_MAXIMUM"))
        # self.ui.tmaxLDoubleSpin.setValue(settings.get("T_LARGE_DEFAULT"))

        # Connecting buttons
        self.ui.buttonOpen.clicked.connect(self.openFile)
        self.ui.buttonSave.clicked.connect(self.saveFile)
        self.ui.buttonCheck.clicked.connect(self.checkCode)
        self.ui.buttonAnalyse.clicked.connect(self.analyseCode)
        self.ui.buttonScore.clicked.connect(self.scoreCode)
        self.ui.buttonHelp.clicked.connect(self.displayHelp)

        # Create the matplotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.
        self.sc = MplCanvas(self, width=5, height=4, dpi=100)
        toolbar = NavigationToolbar2QT(self.sc, self)
        self.ui.plot_layout.addWidget(toolbar)
        self.ui.plot_layout.addWidget(self.sc)

        self.xdata = [0,1,2,3,4]
        self.ydata = [0,1,2,3,4]
        self._plot_ref = None
        self.update_plot()

        # Timer
        self.timer = QtCore.QTimer()
        self.timer.setInterval(200)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

    def update_plot(self):
        # Drop off the first y eleme
        self.ydata = self.ydata[1:] + [random.randint(0, 10)]

        if self._plot_ref is None:
            plot_refs = self.sc.axes.plot(self.xdata, self.ydata, 'r')
            self._plot_ref = plot_refs[0]
        else:
            # we have a ref, so we can use it to update the data for that line
            self._plot_ref.set_ydata(self.ydata)

        self.sc.draw()

    @pyqtSlot()
    def openFile(self):
        try:
            self.filename = QtWidgets.QFileDialog.getOpenFileName(None, 'Open code file', "", settings.get("ALLOWED_FILE_EXTENSIONS"))
            if self.filename[0] != '':
                f = open(self.filename[0], 'r')
                data = f.read()
                f.close()
                self.ui.codeEditor.clear()
                self.ui.codeEditor.insertPlainText(data)
        except Exception as e:
            raise(Exception(f"File could not be opened: {e}"))

    @pyqtSlot()
    def saveFile(self):
        try:
            data = self.ui.codeEditor.toPlainText()
            name = QtWidgets.QFileDialog.getSaveFileName(None, 'Save File', ('.py'))
            file = open(name[0] + ".py", 'w')
            file.writelines(data)
            file.close()
        except Exception as e:
            raise (Exception(f"File could not be saved: {e}"))

    @pyqtSlot()
    def checkCode(self):
        print("checkCode")
        pass

    @pyqtSlot()
    def analyseCode(self):
        print("AnaluseCode")
        pass

    @pyqtSlot()
    def scoreCode(self):
        print("scoreCode")
        pass

    @pyqtSlot()
    def displayHelp(self):
        print("displayHelp")
        pass

# if __name__ == '__main__':
#     app = QtWidgets.QApplication([])
#     # app.setAttribute(QtCore.Qt.AA_Use96Dpi)
#     window = BioreactorApp()
#     window.show()
#     app.exec_()