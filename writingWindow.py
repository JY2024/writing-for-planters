import sys

import collapsableBox
import bulletPoint
import customDialog

from PyQt5.QtCore import (
    QSize, QPropertyAnimation, QParallelAnimationGroup
)
from PyQt5 import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QLineEdit, QGroupBox, QPushButton, QScrollArea, QCheckBox
)


# Writing window
class WritingWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(QSize(1000, 700))
        self.setMaximumSize(QSize(1000, 700))
        # Set the window title according to the work title

        # Outline label
        outline_label = QLabel("Outline")
        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        outline_label.setFont(font)

        # Line Edit
        self.lineEdit = QLineEdit()
        self.lineEdit.setMaximumSize(QSize(500, 100))

        # Group box for outline bullet points
        self.groupBox = QGroupBox()
        self.groupBoxLayout = QVBoxLayout()
        self.groupBox.setLayout(self.groupBoxLayout)
        self.groupBox.setMaximumSize(QSize(500, 500))

        # Outline layout
        outline_layout = QHBoxLayout()
        outline_layout.addWidget(self.lineEdit)
        outline_layout.addWidget(self.groupBox)

        # Enter button
        self.enterButton = QPushButton("Enter")
        self.enterButton.setMaximumSize(QSize(100, 30))

        # Remove button
        self.removeButton = QPushButton("Remove")
        self.removeButton.setMaximumSize(QSize(100, 30))
        self.removeButton.setCheckable(True)
        self.removeButton.setChecked(False)

        # Main Layout
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(outline_label)
        self.mainLayout.addLayout(outline_layout)
        self.mainLayout.addWidget(self.enterButton)
        self.mainLayout.addWidget(self.removeButton)

        # Finish layout set up
        widget = QWidget()
        widget.setLayout(self.mainLayout)
        scroll = QScrollArea()
        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)
        self.setCentralWidget(scroll)

        # Connect signals
        self.enterButton.clicked.connect(self.enter_was_clicked)
        self.removeButton.clicked.connect(self.remove_was_clicked)

    # when button is clicked, place text into outline group of buttons
    def enter_was_clicked(self):
        bullet = bulletPoint.BulletPoint(self.lineEdit.text())
        self.groupBoxLayout.addLayout(bullet)
        box = collapsableBox.CollapsableBox(self.lineEdit.text())
        self.mainLayout.addWidget(box)
        self.lineEdit.setText("")

    # when button is clicked, show the checkboxes next to the bullet points
    def remove_was_clicked(self):
        if self.removeButton.isChecked():
            self.toggle_all_checkboxes()
            self.enterButton.setDisabled(True)
        else:
            if self.at_least_one_checked():
                dlg = customDialog.CustomDialog(self)
                dlg.exec()
            else:
                self.revert_remove_mode()

    # returns whether at least one bullet point is checked off
    def at_least_one_checked(self):
        for bullet in self.groupBox.findChildren(bulletPoint.BulletPoint):
            if bullet.checkBox_selected():
                return True
        return False

    # change back to state before remove mode was enabled
    def revert_remove_mode(self):
        self.removeButton.setChecked(False)
        self.toggle_all_checkboxes()
        self.enterButton.setDisabled(False)

    def toggle_all_checkboxes(self):
        for bullet in self.groupBox.findChildren(bulletPoint.BulletPoint):
            bullet.toggle_checkbox()

    def on_ok(self):
        for bullet in self.groupBox.findChildren(bulletPoint.BulletPoint):
            if bullet.checkBox_selected():
                box = self.find_matching_box(bullet)
                if box != None:
                    self.mainLayout.removeWidget(box)
                    bullet.removeItems()
                    self.groupBoxLayout.removeItem(bullet)
        self.revert_remove_mode()

    def on_reject(self):
        pass

    def find_matching_box(self, bullet):
        for i in range(self.mainLayout.count()):
            item = self.mainLayout.itemAt(i).widget()
            if item != None and item.text() == bullet.text():
                return item
        return None