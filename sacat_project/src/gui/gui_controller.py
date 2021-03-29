"""
SACAT
Sorting Algorithm Complexity Analyser Tool
"""

from gui_model import *

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    # Some time ago I used the line below, but I forgot what it does
    #app.setAttribute(QtCore.Qt.AA_Use96Dpi)
    window = SacatApp()
    window.show()
    app.exec_()