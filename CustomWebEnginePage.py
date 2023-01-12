from PySide2.QtWebEngineWidgets import QWebEnginePage
from PySide2.QtWidgets import QLabel, QToolTip
from PySide2.QtGui import QCursor
from PySide2.QtGui import QFont
from PySide2.QtCore import QTimer
from Dictionary import Dictionary

class CustomWebEnginePage(QWebEnginePage):
    def __init__(self, view):
        super().__init__()
        self.view = view
        font = QFont()
        font.setPointSize(18)
        font.setFamily("Arial")
        font.setBold(True)
        QToolTip.setFont(font)
        
        # Connect the loadFinished signal to a slot
        self.loadFinished.connect(self.on_load_finished)

        self.dictionary = Dictionary()
        self.dictionary.set_dictionary(self.dictionary.dictionary_list[3])
        
        # Create a QTimer and set its timeout signal to trigger the show_tooltip function
        self.tooltip_timer = QTimer()
        self.tooltip_timer.setInterval(500)
        self.tooltip_timer.timeout.connect(self.show_tooltip)
        self.textToShow = ""

    def on_load_finished(self):
        # Define the JavaScript code as a string
        mouseover_function = """
            document.body.addEventListener("mouseover", function(event) 
            {
                console.log("Hovered over element with text: " + event.target.innerText);
            });
        """
        mouseout_function = """
        document.body.addEventListener("mouseout", function(event) {
        console.log("Mouse left element with text: " + event.target.innerText);
        });
        """

        # Run the JavaScript code
        self.runJavaScript(mouseout_function)
        self.runJavaScript(mouseover_function)

    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceId):
        if level == QWebEnginePage.InfoMessageLevel:
            # Extract the text that was hovered over or left
            action, hovered_text = message.split(":")
            hovered_text = hovered_text.strip()

            if action == "Mouse left element with text":
                # Stop the QTimer
                self.tooltip_timer.stop()
                QToolTip.hideText()
            elif action == "Hovered over element with text":
                # Set the text of the tooltip to the hovered text
                # Hide the previous tooltip
                QToolTip.hideText()
                self.textToShow = hovered_text
                result = self.dictionary.look_up(hovered_text)
                #print(result[0].reading)
                #print(result[0].glossary)
                try:
                    self.textToShow += '\n' + "Readings: " + ' '.join(result[0].reading) + '\n' + "Definitions: " + ', '.join(sum(result[0].glossary, []))
                    QToolTip.showText(QCursor.pos(), self.textToShow)
                except:
                    pass
                self.tooltip_timer.start()
            else:
                #print(action)
                pass
    
    def show_tooltip(self):
        QToolTip.showText(QCursor.pos(), self.textToShow)