import sys
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QFile
from PySide2 import QtWidgets
from MainWindow import MainWindow

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
 
    window = MainWindow()
    window.show()
 
    sys.exit(app.exec_())