from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

class WorkSummary(QWidget):
    def __init__(self, parent, title, tags, description):
        super().__init__()
        self.my_parent = parent

        self.setMinimumSize(QSize(500, 400))
        self.setMaximumSize(QSize(500, 400))

        self.titleButton = QPushButton(title)
        self.titleButton.setStyleSheet("background-color:yellow;border:1px solid black;font:bold 20px")
        self.titleButton.setMaximumSize(QSize(400, 50))
        self.tagLabel = QLabel(tags)
        self.tagLabel.setStyleSheet("background-color:white;border:1px solid black;font:14px")
        self.descriptionLabel = QLabel(description)
        self.descriptionLabel.setStyleSheet("background-color:white;border:1px solid black;font:14px")

        self.mainLayout = QVBoxLayout()

        self.mainLayout.addWidget(self.titleButton)
        self.mainLayout.addWidget(self.tagLabel)
        self.mainLayout.addWidget(self.descriptionLabel)
        self.setLayout(self.mainLayout)

        self.titleButton.clicked.connect(self.on_title_clicked)

    def on_title_clicked(self):
        self.my_parent.open_work(self.titleButton.text())


