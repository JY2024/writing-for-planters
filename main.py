import sys

from PyQt5.QtWidgets import QApplication

import worksWindow


def starting_point():
    app = QApplication(sys.argv)
    works_window = worksWindow.WorksWindow()
    works_window.show()
    app.exec()


if __name__ == '__main__':
    starting_point()