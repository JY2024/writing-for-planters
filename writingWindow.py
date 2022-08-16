import sys

import collapsableBox
import bulletPoint
import customDialog
import editWindow

from PyQt5.QtCore import (
    QSize, QPoint
)
from PyQt5 import Qt
from PyQt5.QtGui import QFont, QKeySequence
from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QLineEdit, QGroupBox, QPushButton, QScrollArea
)


# Writing window
class WritingWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(QSize(1000, 700))
        self.setMaximumSize(QSize(1000, 700))
        # Set the window title according to the work title

        # Outline and Story labels
        outline_label = QLabel("Outline")
        story_label = QLabel("Story")
        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        outline_label.setFont(font)
        story_label.setFont(font)

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

        # Buttons
        self.enterButton = self.generate_button("Enter", False)
        self.removeButton = self.generate_button("Remove", True)
        self.toggleBoxesButton = self.generate_button("Expand All", True)
        self.editButton = self.generate_button("Edit", False)

        # Main Layout
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(outline_label)
        self.mainLayout.addLayout(outline_layout)
        self.mainLayout.addWidget(self.enterButton)
        self.mainLayout.addWidget(self.removeButton)
        self.mainLayout.addWidget(self.editButton)
        self.mainLayout.addWidget(story_label)
        self.mainLayout.addWidget(self.toggleBoxesButton)

        # Finish layout set up
        widget = QWidget()
        widget.setLayout(self.mainLayout)
        self.scroll = QScrollArea()
        self.scroll.setWidget(widget)
        self.scroll.setWidgetResizable(True)
        self.setCentralWidget(self.scroll)

        # Connect signals
        self.enterButton.clicked.connect(self.enter_was_clicked)
        self.removeButton.clicked.connect(self.remove_was_clicked)
        self.toggleBoxesButton.clicked.connect(self.toggle_boxes_clicked)
        self.editButton.clicked.connect(self.on_enter_edit_ok)

    def generate_button(self, text, checkable):
        button = QPushButton(text)
        button.setMaximumSize(QSize(100, 30))
        if checkable:
            button.setCheckable(True)
            button.setChecked(False)
        return button

    # when button is clicked, place text into outline group of buttons
    def enter_was_clicked(self):
        text = self.lineEdit.text()
        if self.is_duplicate_bullet(text):
            dlg = customDialog.CustomDialog(
                self, "Duplicate Bulletpoint", "You already have a bulletpoint with this name.\nDo you want to reorder instead?", self.on_enter_edit_ok, self.on_enter_edit_reject
            )
            dlg.exec()
        else:
            bullet = bulletPoint.BulletPoint(text, self)
            self.groupBoxLayout.addLayout(bullet)
            box = collapsableBox.CollapsableBox(text)
            self.mainLayout.addWidget(box)
            self.lineEdit.setText("")

    # when button is clicked, show the checkboxes next to the bullet points
    def remove_was_clicked(self):
        if self.removeButton.isChecked():
            self.toggle_all_checkboxes()
            self.enterButton.setDisabled(True)
        else:
            if self.at_least_one_checked():
                dlg = customDialog.CustomDialog(
                    self, "Deletion", "Are you sure you want to delete this?\nTHIS IS NOT REVERSIBLE", self.on_delete_ok, self.revert_remove_mode
                )
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
        self.uncheck_all()
        self.enterButton.setDisabled(False)

    def toggle_all_checkboxes(self):
        for bullet in self.groupBox.findChildren(bulletPoint.BulletPoint):
            bullet.toggle_checkbox()

    def uncheck_all(self):
        for bullet in self.groupBox.findChildren(bulletPoint.BulletPoint):
            if bullet.checkBox_selected():
                bullet.uncheck()

    def on_delete_ok(self):
        for bullet in self.groupBox.findChildren(bulletPoint.BulletPoint):
            if bullet.checkBox_selected():
                box = self.find_matching_box(bullet)
                if box != None:
                    self.mainLayout.removeWidget(box)
                    bullet.removeItems()
                    self.groupBoxLayout.removeItem(bullet)
        self.revert_remove_mode()

    def find_matching_box(self, bullet):
        for i in range(self.mainLayout.count()):
            item = self.mainLayout.itemAt(i).widget()
            if item != None and item.text() == bullet.text():
                return item
        return None

    def bulletPoint_was_clicked(self, bullet):
        box = self.find_matching_box(bullet)
        self.scroll.ensureWidgetVisible(box)

    def toggle_boxes_clicked(self):
        cond = lambda bool: not bool if self.toggleBoxesButton.isChecked() else bool
        setTxt = lambda: "Collapse All" if self.toggleBoxesButton.isChecked() else "Expand All"
        self.toggleBoxesButton.setText(setTxt())
        for i in range(self.mainLayout.count()):
            item = self.mainLayout.itemAt(i).widget()
            if isinstance(item, collapsableBox.CollapsableBox) and cond(item.get_checked()):
                item.toggle_checked()
                item.button_was_clicked()

    def is_duplicate_bullet(self, text):
        for bullet in self.groupBox.findChildren(bulletPoint.BulletPoint):
            if bullet.get_text() == text:
                return True
        return False

    def on_enter_edit_ok(self):
        dlg = editWindow.EditWindow()
        dlg.exec()

    def on_enter_edit_reject(self):
        self.lineEdit.clear()