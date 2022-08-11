import sys
from PyQt5.QtCore import (
    QSize, Qt
)
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QLineEdit, QGroupBox, QPushButton
)


# Writing window
class WritingWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(QSize(1000, 700))
        self.setMaximumSize(QSize(1000, 700))
        # Set the window title according to the work title

        # Outline layout
        outline_layout = QHBoxLayout()
        self.lineEdit = QLineEdit() # START HERE
        self.lineEdit.setMaximumSize(QSize(500, 100))
        self.groupBox = QGroupBox()
        self.groupBoxLayout = QVBoxLayout()
        self.groupBox.setLayout(self.groupBoxLayout)
        self.groupBox.setMaximumSize(QSize(500, 500))
        outline_layout.addWidget(self.lineEdit)
        outline_layout.addWidget(self.groupBox) # for buttons

        # Main Layout
        main_layout = QVBoxLayout()
        outline_label = QLabel("Outline")
        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        outline_label.setFont(font)

        button = QPushButton("Enter")
        button.setMaximumSize(QSize(100, 30))

        main_layout.addWidget(outline_label)
        main_layout.addLayout(outline_layout)
        main_layout.addWidget(button)

        # Finish layout set up
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

        # Connect signals
        button.clicked.connect(self.button_was_clicked)

    # when button is clicked, place text into outline group of buttons
    def button_was_clicked(self):
        bullet = QPushButton(self.lineEdit.text())
        self.groupBoxLayout.addWidget(bullet)
