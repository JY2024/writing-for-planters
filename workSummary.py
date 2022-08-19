from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QCheckBox

import designFunctions


class WorkSummary(QWidget):
    def __init__(self, parent, title, tags, description):
        super().__init__()
        self.my_parent = parent

        self.setMinimumSize(QSize(500, 400))
        self.setMaximumSize(QSize(500, 400))

        self.topLayout = QHBoxLayout()

        self.titleButton = designFunctions.generate_button(title, background_color="yellow", border=True, bold=True, font_size="20px", size=QSize(400, 50))
        self.topLayout.addWidget(self.titleButton)
        self.checkBox = QCheckBox()
        self.checkBox.hide()
        self.topLayout.addWidget(self.checkBox)
        self.tagLabel = designFunctions.generate_label(tags, border=True, font_size="14px")
        self.descriptionLabel = designFunctions.generate_label(border=True, font_size="14px")

        self.mainLayout = QVBoxLayout()

        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addWidget(self.tagLabel)
        self.mainLayout.addWidget(self.descriptionLabel)
        self.setLayout(self.mainLayout)

        self.titleButton.clicked.connect(self.on_title_clicked)

    def on_title_clicked(self):
        self.my_parent.open_work(self.titleButton.text())

    def toggle_checkbox_visible(self):
        if self.checkBox.isVisible():
            self.checkBox.hide()
        else:
            self.checkBox.show()

    def is_checked(self):
        return self.checkBox.isChecked()

    def get_title(self):
        return self.titleButton.text()

