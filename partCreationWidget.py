from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QTextEdit, QLabel


class PartCreationWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.title = QLineEdit()
        self.synopsis = QTextEdit()
        self.layout.addWidget(self.generate_label("Part Title"))
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.generate_label("Synopsis"))
        self.layout.addWidget(self.synopsis)
        self.setLayout(self.layout)

    def generate_label(self, text):
        label = QLabel(text)
        label.setFixedSize(100, 50)
        return label

    def get_title(self):
        return self.title.text()

    def get_description(self):
        return self.synopsis.toPlainText()