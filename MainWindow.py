import sys
from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui
from PySide2.QtGui import QPixmap, QImage, QIcon
from PySide2.QtWebEngineWidgets import *
from Dictionary import Dictionary
from Furigana import Furigana
from CustomWebEnginePage import CustomWebEnginePage
from JapaneseWord import JapaneseWord
import itertools
from datetime import datetime
from googletrans import Translator

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
        self.translator = Translator()
 
 
    def initGui(self):
        self.layout = QtWidgets.QGridLayout()
        self.window = QtWidgets.QWidget()
        self.window.setLayout(self.layout)
        self.setCentralWidget(self.window)

        self.leSearch = QtWidgets.QLineEdit()
        self.tvLookup = QtWidgets.QTableWidget()
        self.tvLookupHeader=self.tvLookup.horizontalHeader()
        self.tvLookupHeader.setStretchLastSection(True)
        self.teDisplay = QWebEngineView(self)
        self.teTranslate = QtWidgets.QTextEdit()
        self.teTranslate.setVisible(False)
        self.teTranslate.setFontPointSize(18)
        self.teTranslate.setMaximumHeight(200)
        self.chkTranslate = QtWidgets.QCheckBox("Google Translate")
        self.chkTranslate.setChecked(False)
        self.chkDisplay = QtWidgets.QCheckBox("Intelligent Display")
        self.chkDisplay.setChecked(True)

        self.customWebEngineView = CustomWebEnginePage(self.teDisplay)
        self.teDisplay.setPage(self.customWebEngineView)

        #self.teDisplay.load("/home/steve/Projects/Manji/readme.md")
        self.customWebEngineView.setHtml("<html style='background-color: #101013; color: white; font-size: 30px;'></html>")
        self.teDisplay.setMinimumHeight(300)
        self.teDisplay.show()
        #self.teDisplay.setFontPointSize(28)

        self.pbSearch = QtWidgets.QPushButton("search")
        self.pbBack = QtWidgets.QPushButton()
        self.pbNext = QtWidgets.QPushButton()
        self.pbOptions = QtWidgets.QPushButton()

        self.pbOptions.clicked.connect(self.openOptions)
        self.pbBack.clicked.connect(self.pbBackClicked)
        self.pbNext.clicked.connect(self.pbNextClicked)
        self.pbSearch.clicked.connect(self.pbSearchClicked)
        self.chkTranslate.stateChanged.connect(self.translateChecked)
        self.chkDisplay.stateChanged.connect(self.displayChecked)

        # Starting events
        self.chkTranslate.setChecked(True)

        pbBackImage = QPixmap("res/images/back_button_icon.png")
        pbForwardImage = QPixmap("res/images/forward_button_icon.png")
        pbOptionsImage = QPixmap("res/images/options_button.png")
        pbSearchImage = QPixmap("res/images/search_button.png")

        self.pbOptions.setIcon(QIcon(pbOptionsImage))
        self.pbOptions.setFlat(True)
        self.pbOptions.setIconSize(QtCore.QSize(24, 24))
        self.pbBack.setIcon(QIcon(pbBackImage))
        self.pbBack.setFlat(True)
        self.pbBack.setIconSize(QtCore.QSize(24, 24))
        self.pbNext.setIcon(QIcon(pbForwardImage))
        self.pbNext.setFlat(True)
        self.pbNext.setIconSize(QtCore.QSize(24, 24))
        self.pbSearch.setIcon(QIcon(pbSearchImage))
        self.pbSearch.setFlat(True)
        self.pbSearch.setIconSize(QtCore.QSize(24, 24))

        self.layout.addWidget(self.pbOptions, 0, 0)
        self.layout.addWidget(self.pbBack,   0, 1)
        self.layout.addWidget(self.pbNext,   0, 2)
        self.layout.addWidget(self.leSearch, 0, 3)
        self.layout.addWidget(self.pbSearch, 0, 4)
        self.layout.addWidget(self.tvLookup, 1, 0, 1, 5)
        self.layout.addWidget(self.teDisplay, 2, 0, 1, 5)
        self.layout.addWidget(self.teTranslate, 3, 0, 1, 5)
 
    def pbSearchClicked(self):
        self.tvLookup.clear()
        incomingText = self.leSearch.text()
        if self.contains_japanese(incomingText):        
            if incomingText not in self.dictionary.search_history:
                self.dictionary.search_history.append(incomingText)
                self.dictionary.search_index = len(self.dictionary.search_history) - 1
            
            result = self.dictionary.look_up(incomingText)
            #print(result[0].reading)
            
            row_count = (len(result))
            column_count = 5
            self.tvLookup.setColumnCount(column_count) 
            self.tvLookup.setRowCount(row_count)

            header_labels = [key for key in vars(JapaneseWord) if not key.startswith('__')]
            self.tvLookup.setHorizontalHeaderLabels(header_labels)
            #self.tvLookup.setHorizontalHeaderLabels((list(result[0].__dict__keys())))
            self.tvLookup.setColumnWidth(3, 460)
            
            modified_row_counter = 0
            for row in range(len(result)):
                if result[row].reading is not None and result[row].reading != [''] and result[row].reading != []:
                    #print(result[row].reading)
                    self.tvLookup.setItem(modified_row_counter, 0, QtWidgets.QTableWidgetItem(result[row].headword))
                    self.tvLookup.setItem(modified_row_counter, 1, QtWidgets.QTableWidgetItem(", ".join([x for x in result[row].reading if x != ''])))
                    self.tvLookup.setItem(modified_row_counter, 2, QtWidgets.QTableWidgetItem(", ".join(result[row].tags)))
                    self.tvLookup.setItem(modified_row_counter, 3, QtWidgets.QTableWidgetItem(", ".join(result[row].sequence)))
                    self.tvLookup.setItem(modified_row_counter, 4, QtWidgets.QTableWidgetItem(", ".join(list(itertools.chain.from_iterable(result[row].glossary)))))
                    modified_row_counter += 1
            self.tvLookup.setRowCount(modified_row_counter)
            self.tvLookup.resizeColumnsToContents()
            
            if self.teDisplay.isVisible():
                self.customWebEngineView.setHtml(self.furigana_reader.addFurigana(result))

            if self.teTranslate.isVisible():
                    self.teTranslate.setText(self.translateText(incomingText))
        else:
            self.leSearch.clear()

    def pbBackClicked(self):
        if self.dictionary.search_index > 0:
            self.dictionary.search_index -= 1
            self.leSearch.setText(self.dictionary.search_history[self.dictionary.search_index])

    def pbNextClicked(self):
        if self.dictionary.search_index < len(self.dictionary.search_history) - 1:
            self.dictionary.search_index += 1
            self.leSearch.setText(self.dictionary.search_history[self.dictionary.search_index])
    
    def pbSaveClicked(self):
        f = open("res/logs/log-" + str(datetime.now()), 'w')
        f.writelines(self.dictionary.search_history)
        f.close()

    def clipboardChanged(self):
        self.leSearch.setText(QtWidgets.QApplication.clipboard().text())
        self.pbSearchClicked()

    def openOptions(self):
        optionsWindow = QtWidgets.QMainWindow(self)
        optionsWindow.setWindowTitle('Options')
        optionsWindow.resize(300, 200)

        # Set up the layout and widgets for the options window
        optionsLayout = QtWidgets.QVBoxLayout()
        optionsWidget = QtWidgets.QWidget()
        optionsWidget.setLayout(optionsLayout)
        optionsWindow.setCentralWidget(optionsWidget)

        # Layout Customizations
        optionsLayout.addWidget(self.chkDisplay)
        optionsLayout.addWidget(self.chkTranslate)

        # Add a "Save log" button to the options window
        saveLogButton = QtWidgets.QPushButton("Save log")
        saveLogButton.clicked.connect(self.pbSaveClicked)  # Connect the clicked signal to the pbSaveClicked slot
        optionsLayout.addWidget(saveLogButton)


        # Show the options window
        optionsWindow.show()

    def translateChecked(self, state):
        if state == QtCore.Qt.Checked:
            self.teTranslate.setVisible(True)
        else:
            # do nothing or reset the text
            self.teTranslate.setVisible(False)

    def displayChecked(self, state):
        if state == QtCore.Qt.Checked:
            self.teDisplay.setVisible(True)
        else:
            # do nothing or reset the text
            self.teDisplay.setVisible(False)

    def translateText(self, text):
        
        text = text.replace("\n", "")
        text = text.replace("\r\n", "")
        #print(text)
        return self.translator.translate(text, src='ja', dest='en').__dict__()["text"]

    def contains_japanese(self, text):
        return any(3040 <= ord(c) <= 0x30FF or ord(c) >= 0x3040 for c in text)
