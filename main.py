import sys

import worksWindow
import writingWindow
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)
# writing_window = writingWindow.WritingWindow()
# writing_window.show()

works_window = worksWindow.WorksWindow()
works_window.show()

app.exec()
