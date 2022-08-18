from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QCheckBox, QLabel, QVBoxLayout


class PartSummary(QWidget):
    def __init__(self, parent, title, synopsis, partNumber):
        super().__init__()
        self.my_parent = parent
        self.title = title

        self.setMinimumSize(QSize(500, 400))
        self.setMaximumSize(QSize(500, 400))

        self.topLayout = QHBoxLayout()

        self.titleButton = QPushButton("Part " + str(partNumber) + ": " +title)
        self.titleButton.setStyleSheet("background-color:white;border:1px solid black;font:bold 20px")
        self.titleButton.setMaximumSize(QSize(400, 50))
        self.topLayout.addWidget(self.titleButton)
        # Completion status
        self.checkBox = QCheckBox()
        self.checkBox.hide()
        self.topLayout.addWidget(self.checkBox)
        self.synopsisLabel = QLabel(synopsis)
        self.synopsisLabel.setStyleSheet("background-color:white;border:1px solid black;font:14px")

        self.mainLayout = QVBoxLayout()

        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addWidget(self.synopsisLabel)
        self.setLayout(self.mainLayout)

        self.titleButton.clicked.connect(self.on_title_clicked)

    def on_title_clicked(self):
        self.my_parent.open_part(self.title)