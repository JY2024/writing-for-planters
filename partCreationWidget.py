import designFunctions

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QTextEdit, QLabel


class PartCreationWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.title = QLineEdit()
        self.synopsis = QTextEdit()

        self.layout.addWidget(designFunctions.generate_label("Part Title", size=QSize(100, 50)))
        self.layout.addWidget(self.title)
        self.layout.addWidget(designFunctions.generate_label("Synopsis", size=QSize(100, 50)))
        self.layout.addWidget(self.synopsis)
        self.setLayout(self.layout)

    def get_title(self):
        return self.title.text()

    def get_description(self):
        return self.synopsis.toPlainText()