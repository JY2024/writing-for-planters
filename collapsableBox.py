from PyQt5.QtWidgets import (
    QVBoxLayout, QPushButton, QTextEdit, QWidget
)


class CollapsableBox(QWidget):
    def __init__(self, text):
        # Set up
        super().__init__()
        layout = QVBoxLayout()
        button = QPushButton(text)
        self.textEdit = QTextEdit()
        self.textEdit.setMinimumHeight(500)
        layout.addWidget(button)
        layout.addWidget(self.textEdit)

        # Animation

        button.clicked.connect(self.button_was_clicked)

        self.setLayout(layout)

    def button_was_clicked(self):
        pass
