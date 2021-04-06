"""
SACAT
Sorting Algorithm Complexity Analyser Tool
"""
import sys
from src.gui.gui_model import *

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = SacatApp()
    window.show()
    app.exec_()
    sys.exit()
