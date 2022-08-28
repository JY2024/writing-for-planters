import sys

import worksWindow
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)

works_window = worksWindow.WorksWindow()
works_window.show()

app.aboutToQuit.connect(works_window.closeEvent)

app.exec()
