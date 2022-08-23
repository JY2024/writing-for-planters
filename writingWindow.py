import collapsableBox
import bulletPoint
import customDialog
import editWindow
import designFunctions
import scrollableWindow

from PyQt5.QtCore import (
    QSize
)
from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QGroupBox
)

# Writing window
class WritingWindow(scrollableWindow.ScrollableWindow):
    def __init__(self, title):
        self.num_parts = 0
        # Outline and Story labels
        outline_label = designFunctions.generate_label("Outline", bold=True, font_size="20px")
        story_label = designFunctions.generate_label("Story", bold=True, font_size="20px")

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
        self.enterButton = designFunctions.generate_button("Enter", checkable=False)
        self.removeButton = designFunctions.generate_button("Remove", checkable=True)
        self.toggleBoxesButton = designFunctions.generate_button("Expand All", checkable=True)
        self.editButton = designFunctions.generate_button("Edit", checkable=False)

        # Group box for collapsable boxes
        self.box_for_boxes = QGroupBox()
        self.boxes_layout = QVBoxLayout()
        self.box_for_boxes.setLayout(self.boxes_layout)

        # Main Layout
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(outline_label)
        self.mainLayout.addLayout(outline_layout)
        self.mainLayout.addWidget(self.enterButton)
        self.mainLayout.addWidget(self.removeButton)
        self.mainLayout.addWidget(self.editButton)
        self.mainLayout.addWidget(story_label)
        self.mainLayout.addWidget(self.toggleBoxesButton)
        self.mainLayout.addWidget(self.box_for_boxes)

        super().__init__(title, QSize(1000, 700), self.mainLayout)

        # Connect signals
        self.enterButton.clicked.connect(self.enter_was_clicked)
        self.removeButton.clicked.connect(self.remove_was_clicked)
        self.toggleBoxesButton.clicked.connect(self.toggle_boxes_clicked)
        self.editButton.clicked.connect(self.on_enter_edit_ok)

        self.firstBoxIndex = None

    # when button is clicked, place text into outline group of buttons
    def enter_was_clicked(self):
        text = self.lineEdit.text()
        if self.is_duplicate_bullet(text):
            dlg = customDialog.CustomDialog(
                self, "Duplicate Bulletpoint", QSize(300, 100), QLabel("You already have a bulletpoint with this name.\nDo you want to reorder instead?"), self.on_enter_edit_ok, self.on_edit_reject
            )
            dlg.exec()
        else:
            self.num_parts += 1
            box = collapsableBox.CollapsableBox(text)
            self.boxes_layout.addWidget(box)
            bullet = bulletPoint.BulletPoint(text, self, box, self.num_parts)
            self.groupBoxLayout.addLayout(bullet)
            if self.firstBoxIndex == None:
                self.firstBoxIndex = self.boxes_layout.indexOf(box)
            self.lineEdit.setText("")

    # when button is clicked, show the checkboxes next to the bullet points
    def remove_was_clicked(self):
        if self.removeButton.isChecked():
            self.toggle_all_checkboxes()
            self.enterButton.setDisabled(True)
            self.editButton.setDisabled(True)
        else:
            if self.at_least_one_checked():
                dlg = customDialog.CustomDialog(
                    self, "Deletion", QSize(300, 100), QLabel("Are you sure you want to delete this?\nTHIS IS NOT REVERSIBLE"), self.on_delete_ok, self.revert_remove_mode
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
        self.editButton.setDisabled(False)

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
                box = self.find_matching_box(bullet.get_text())
                if box != None:
                    self.mainLayout.removeWidget(box)
                    bullet.removeItems()
                    self.groupBoxLayout.removeItem(bullet)
        self.revert_remove_mode()

    def find_matching_box(self, text):
        for i in range(self.boxes_layout.count()):
            item = self.boxes_layout.itemAt(i).widget()
            if item != None and item.text() == text:
                return item
        return None

    def bulletPoint_was_clicked(self, bullet):
        box = self.find_matching_box(bullet.get_text())
        self.scroll.ensureWidgetVisible(box)

    def toggle_boxes_clicked(self):
        cond = lambda bool: not bool if self.toggleBoxesButton.isChecked() else bool
        setTxt = lambda: "Collapse All" if self.toggleBoxesButton.isChecked() else "Expand All"
        self.toggleBoxesButton.setText(setTxt())
        for i in range(self.boxes_layout.count()):
            item = self.boxes_layout.itemAt(i).widget()
            if isinstance(item, collapsableBox.CollapsableBox) and cond(item.get_checked()):
                item.toggle_checked()
                item.button_was_clicked()

    def is_duplicate_bullet(self, text):
        for bullet in self.groupBox.findChildren(bulletPoint.BulletPoint):
            if bullet.get_text() == text:
                return True
        return False

    def on_enter_edit_ok(self):
        edit = editWindow.EditWindow(self.groupBox.findChildren(bulletPoint.BulletPoint))
        dlg = customDialog.CustomDialog(
            self, "Edit", QSize(400, 700), edit, self.on_edit_ok, self.on_edit_reject
        )
        dlg.exec()

    def on_edit_reject(self):
        self.lineEdit.clear()

    def on_edit_ok(self, widget):
        # Change box names


        # Change bulletpoint buttons texts
        bulletPoints = self.groupBox.findChildren(bulletPoint.BulletPoint)
        lineEdits = widget.sorted_children()
        for (bullet, lineEdit) in zip(bulletPoints, lineEdits):
            bullet.set_text(lineEdit.text())

        # Reorder the boxes
        for i in range(len(lineEdits)):
            targetIndex = self.firstBoxIndex + i
            box = self.find_matching_box(lineEdits[i].text())
            indexOfBox = self.boxes_layout.indexOf(box)
            if indexOfBox != targetIndex:
                temp = self.boxes_layout.itemAt(targetIndex).widget()
                self.boxes_layout.takeAt(targetIndex)
                self.boxes_layout.takeAt(indexOfBox)
                self.boxes_layout.insertWidget(targetIndex, box)
                self.boxes_layout.insertWidget(indexOfBox, temp)
