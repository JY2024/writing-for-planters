from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QTextEdit, QLabel


class WorkCreationWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.title = QLineEdit()
        self.tags = QTextEdit()
        self.description = QTextEdit()
        self.layout.addWidget(self.generate_label("Title"))
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.generate_label("Tags"))
        self.layout.addWidget(self.tags)
        self.layout.addWidget(self.generate_label("Description"))
        self.layout.addWidget(self.description)
        self.setLayout(self.layout)

    def generate_label(self, text):
        label = QLabel(text)
        label.setFixedSize(100, 50)
        return label

    def get_title(self):
        return self.title.text()

    def get_tags(self):
        return self.tags.toPlainText()

    def get_description(self):
        return self.description.toPlainText()