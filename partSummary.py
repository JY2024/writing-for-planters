import designFunctions

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QCheckBox, QLabel, QVBoxLayout


class PartSummary(QWidget):
    def __init__(self, parent, title, synopsis, partNumber):
        super().__init__()
        self.my_parent = parent
        self.title = title

        self.setMinimumSize(QSize(500, 400))
        self.setMaximumSize(QSize(500, 400))

        self.topLayout = QHBoxLayout()
        self.titleButton = designFunctions.generate_button(
            "Part " + str(partNumber) + ": " + title, bold=True, border=True, size=QSize(400, 50)
        )
        self.topLayout.addWidget(self.titleButton)
        # Completion status
        self.checkBox = QCheckBox()
        self.checkBox.hide()
        self.topLayout.addWidget(self.checkBox)
        self.synopsisLabel = designFunctions.generate_label(synopsis, font_size="14px", border=True)

        self.mainLayout = QVBoxLayout()

        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addWidget(self.synopsisLabel)
        self.setLayout(self.mainLayout)

        self.titleButton.clicked.connect(self.on_title_clicked)

    def on_title_clicked(self):
        self.my_parent.open_part(self.title)