from PyQt5.QtCore import QSize
from PyQt5.QtGui import QTextDocument
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QTextEdit, QLabel

import designFunctions


class WorkCreationWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.title = QLineEdit()
        self.title.setStyleSheet("background-color: white")
        self.tags = QTextEdit()
        self.tags.setStyleSheet("background-color: white")
        self.description = QTextEdit()
        self.description.setStyleSheet("background-color: white")

        self.layout.addWidget(designFunctions.generate_label("Title", size=QSize(100, 50)))
        self.layout.addWidget(self.title)
        self.layout.addWidget(designFunctions.generate_label("Tags", size=QSize(100, 50)))
        self.layout.addWidget(self.tags)
        self.layout.addWidget(designFunctions.generate_label("Description", size=QSize(100, 50)))
        self.layout.addWidget(self.description)
        self.setLayout(self.layout)

    def get_title(self):
        return self.title.text()

    def get_tags(self):
        doc = QTextDocument()
        doc.setPlainText(self.tags.toPlainText())
        return doc

    def get_description(self):
        doc = QTextDocument()
        doc.setPlainText(self.description.toPlainText())
        return doc