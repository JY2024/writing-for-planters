from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel


class WorkSummary(QWidget):
    def __init__(self, title, tags, description):
        super().__init__()

        self.setMinimumSize(QSize(500, 400))
        self.setMaximumSize(QSize(500, 400))

        self.titleLabel = QLabel(title)
        self.titleLabel.setStyleSheet("background-color:yellow;border:1px solid black;font:bold 20px")
        self.titleLabel.setMaximumSize(QSize(400, 50))
        self.tagLabel = QLabel(tags)
        self.tagLabel.setStyleSheet("background-color:white;border:1px solid black;font:14px")
        self.descriptionLabel = QLabel(description)
        self.descriptionLabel.setStyleSheet("background-color:white;border:1px solid black;font:14px")

        self.mainLayout = QVBoxLayout()

        self.mainLayout.addWidget(self.titleLabel)
        self.mainLayout.addWidget(self.tagLabel)
        self.mainLayout.addWidget(self.descriptionLabel)
        self.setLayout(self.mainLayout)


