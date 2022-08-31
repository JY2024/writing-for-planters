import sys

from PyQt5.QtWidgets import QApplication

import worksWindow

app = QApplication(sys.argv)
works_window = worksWindow.WorksWindow()
works_window.show()
app.exec()
