from PyQt5.QtCore import QSize
from PyQt5.QtGui import QTextDocument
from PyQt5.QtWidgets import QLineEdit, QTextEdit, QVBoxLayout, QWidget

import designFunctions


class PartCreationWidget(QWidget):
    """QWidget to assist in work part creation process"""
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.title = QLineEdit()
        self.synopsis = QTextEdit()
        self.init_ui()

    def init_ui(self):
        """Initializes UI for PartCreationWidget"""
        self.title.setStyleSheet("background-color: rgb(243,240,240)")
        self.synopsis.setStyleSheet("background-color: rgb(243,240,240)")
        self.layout.addWidget(designFunctions.generate_label("Part Title", size=QSize(100, 50)))
        self.layout.addWidget(self.title)
        self.layout.addWidget(designFunctions.generate_label("Synopsis", size=QSize(100, 50)))
        self.layout.addWidget(self.synopsis)
        self.setLayout(self.layout)

    def get_title(self):
        """Returns title text"""
        return self.title.text()

    def get_synopsis(self):
        """Returns synopsis as QTextDocument"""
        doc = QTextDocument()
        doc.setPlainText(self.synopsis.toPlainText())
        return doc