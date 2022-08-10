import sys
from PyQt5.Qt import (
    QFont
)
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QWidget
)

# Writing window
class WritingWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1000, 700)
        # Set the window title according to the work title

        # Layouts
        main_layout = QVBoxLayout()
        outline_layout = QHBoxLayout()

        # Outline Layout

        # Main Layout
        outline_label = QLabel("Outline")
        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        outline_label.setFont(font)
        main_layout.addWidget(outline_label)

        # Set up
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)