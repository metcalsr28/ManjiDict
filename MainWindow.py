import sys
from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui
from PySide2.QtWebEngineWidgets import *
from Dictionary import Dictionary
from Furigana import Furigana

class MainWindow(QtWidgets.QMainWindow):
 
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setWindowTitle('Manji Dict')
        self.resize(1024, 720)
        self.initGui()
        self.dictionary = Dictionary()
        self.dictionary.set_dictionary(self.dictionary.dictionary_list[3])
        QtWidgets.QApplication.clipboard().dataChanged.connect(self.clipboardChanged)
        self.furigana_reader = Furigana()
 
 
    def initGui(self):
        self.layout = QtWidgets.QGridLayout()
        self.window = QtWidgets.QWidget()
        self.window.setLayout(self.layout)
        self.setCentralWidget(self.window)
 
        self.leSearch = QtWidgets.QLineEdit()
        self.tvLookup = QtWidgets.QTableWidget()
        self.teDisplay = QWebEngineView()
        #self.teDisplay.load("/home/steve/Projects/Manji/readme.md")
        self.teDisplay.setHtml("<html style='background-color: #101013; color: white; font-size: 30px;'></html>")
        self.teDisplay.show()
        #self.teDisplay.setFontPointSize(28)

        self.pbSearch = QtWidgets.QPushButton("Search")
        self.pbSearch.clicked.connect(self.pbSearchClicked)
 
        self.layout.addWidget(self.leSearch, 0, 0)
        self.layout.addWidget(self.pbSearch, 0, 1)
        self.layout.addWidget(self.tvLookup, 1, 0, 1, 2)
        self.layout.addWidget(self.teDisplay, 2, 0, 1, 2)
 
    def pbSearchClicked(self):
        tokens, result = self.dictionary.look_up(self.leSearch.text())
        row_count = (len(result))
        column_count = (len(result[0]))
        self.tvLookup.setColumnCount(column_count) 
        self.tvLookup.setRowCount(row_count)
        self.tvLookup.setHorizontalHeaderLabels((list(result[0].keys())))
        self.tvLookup.setColumnWidth(3, 460)
        
        for row in range(row_count):
            for column in range(column_count):
                item = (list(result[row].values())[column])
                self.tvLookup.setItem(row, column, QtWidgets.QTableWidgetItem(str(item)))

        self.teDisplay.setHtml(self.furigana_reader.addFurigana(tokens))

    def clipboardChanged(self):
        self.leSearch.setText(QtWidgets.QApplication.clipboard().text())
        self.pbSearchClicked()
