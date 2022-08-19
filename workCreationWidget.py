from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QTextEdit, QLabel

import designFunctions


class WorkCreationWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.title = QLineEdit()
        self.tags = QTextEdit()
        self.description = QTextEdit()

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
        return self.tags.toPlainText()

    def get_description(self):
        return self.description.toPlainText()