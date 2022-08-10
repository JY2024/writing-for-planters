import sys
import writingWindow
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)
writing_window = writingWindow.WritingWindow()
writing_window.show()

app.exec()
