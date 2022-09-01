from PyQt5.QtCore import QSize
from PyQt5.QtGui import QTextDocument
from PyQt5.QtWidgets import QLineEdit, QTextEdit, QVBoxLayout, QWidget

import designFunctions


class WorkCreationWidget(QWidget):
    """QWidget for assisting in creation of WorkSummary and WorkPage"""
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.title = QLineEdit()
        self.tags = QTextEdit()
        self.description = QTextEdit()
        self.init_ui()

    def init_ui(self):
        """Initializes UI for WorkCreationWidget"""
        self.title.setStyleSheet("background-color: rgb(243,240,240)")
        self.tags.setStyleSheet("background-color: rgb(243,240,240)")
        self.description.setStyleSheet("background-color: rgb(243,240,240)")

        self.layout.addWidget(designFunctions.generate_label("Title", size=QSize(100, 50)))
        self.layout.addWidget(self.title)
        self.layout.addWidget(designFunctions.generate_label("Tags", size=QSize(100, 50)))
        self.layout.addWidget(self.tags)
        self.layout.addWidget(designFunctions.generate_label("Description", size=QSize(100, 50)))
        self.layout.addWidget(self.description)
        self.setLayout(self.layout)

    def get_title(self):
        """Returns title: string"""
        return self.title.text()

    def get_tags(self):
        """Returns tags: QTextDocument"""
        doc = QTextDocument()
        doc.setPlainText(self.tags.toPlainText())
        return doc

    def get_description(self):
        """Returns description: QTextDocument"""
        doc = QTextDocument()
        doc.setPlainText(self.description.toPlainText())
        return doc