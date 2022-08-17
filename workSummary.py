from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel


class WorkSummary(QWidget):
    def __init__(self, title, tags, description):
        super().__init__()

        self.mainLayout = QVBoxLayout()
        self.topLayout = QHBoxLayout()
        self.topLayout.addWidget(QLabel(title))
        status = QWidget()
        status.setStyleSheet("color=yellow")
        self.topLayout.addWidget(status)
        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addWidget(QLabel(tags))
        self.mainLayout.addWidget(QLabel(description))
        self.setLayout(self.mainLayout)


