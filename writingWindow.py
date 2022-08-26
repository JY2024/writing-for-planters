from PyQt5 import QtCore
from PyQt5.QtGui import QKeySequence, QCursor, QColorConstants, QColor

import collapsableBox
import bulletPoint
import customDialog
import editWindow
import designFunctions
import scrollableWindow
import checkboxFunctions

from PyQt5.QtCore import (
    QSize, Qt, QPoint
)
from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QGroupBox, QShortcut, QWidget, QComboBox, QMenu, QApplication,
    QColorDialog, QAction
)

# Writing window
class WritingWindow(scrollableWindow.ScrollableWindow):
    def __init__(self, title):
        self.num_parts = 0
        # Outline and Story labels
        self.outline_label = designFunctions.generate_label("Outline", bold=True, font_size="20px")
        story_label = designFunctions.generate_label("Story", bold=True, font_size="20px")

        # Line Edit
        self.line_edit = QLineEdit()
        self.line_edit.setMaximumSize(QSize(500, 100))

        # Group box for outline bullet points
        self.group_box = QGroupBox()
        self.group_box_layout = QVBoxLayout()
        self.group_box.setLayout(self.group_box_layout)
        self.group_box.setMaximumSize(QSize(500, 500))

        # Outline layout
        outline_layout = QHBoxLayout()
        outline_layout.addWidget(self.line_edit)
        outline_layout.addWidget(self.group_box)

        # Buttons
        self.enter_button = designFunctions.generate_button("&Enter", checkable=False)
        self.remove_button = designFunctions.generate_button("Remove", checkable=True)
        self.toggle_boxes_button = designFunctions.generate_button("Expand All", checkable=True)
        self.edit_button = designFunctions.generate_button("Edit", checkable=False)
        self.placeholders_button = designFunctions.generate_button("Manage Placeholders")

        # Group box for collapsable boxes
        self.box_for_boxes = QGroupBox()
        self.boxes_layout = QVBoxLayout()
        self.box_for_boxes.setLayout(self.boxes_layout)

        # Main Layout
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.outline_label)
        self.main_layout.addLayout(outline_layout)
        self.main_layout.addWidget(self.enter_button)
        self.main_layout.addWidget(self.remove_button)
        self.main_layout.addWidget(self.edit_button)
        self.main_layout.addWidget(story_label)
        self.below_story_layout = QHBoxLayout()
        self.below_story_layout.addWidget(self.toggle_boxes_button)
        self.below_story_layout.addWidget(self.placeholders_button)
        self.main_layout.addLayout(self.below_story_layout)
        self.main_layout.addWidget(self.box_for_boxes)

        super().__init__(title, QSize(1000, 700), self.main_layout)

        self.placeholders = PlaceHolderMechanism(self)

        # Connect signals
        self.enter_button.clicked.connect(self.enter_was_clicked)
        self.remove_button.clicked.connect(self.remove_was_clicked)
        self.toggle_boxes_button.clicked.connect(self.toggle_boxes_clicked)
        self.edit_button.clicked.connect(self.on_enter_edit_ok)
        self.placeholders_button.clicked.connect(self.on_placeholders_manage)

        # Shortcuts
        to_top_shortcut = QShortcut(QKeySequence(self.tr("Ctrl+O")), self)
        to_top_shortcut.activated.connect(self.on_to_top)
        placeholder_shortcut = QShortcut(QKeySequence(self.tr("Ctrl+H")), self)
        placeholder_shortcut.activated.connect(self.on_placeholder_requested)

        self.first_box_index = None

    # when button is clicked, place text into outline group of buttons
    def enter_was_clicked(self):
        text = self.line_edit.text()
        if self.is_duplicate_bullet(text):
            dlg = customDialog.CustomDialog(
                self, "Duplicate Bulletpoint", QSize(300, 100), QLabel("You already have a bulletpoint with this name.\nDo you want to reorder instead?"), self.on_enter_edit_ok, self.on_edit_reject
            )
            dlg.exec()
        else:
            self.num_parts += 1
            box = collapsableBox.CollapsableBox(text, self.num_parts)
            self.boxes_layout.addWidget(box)
            bullet = bulletPoint.BulletPoint(text, self, box, self.num_parts)
            self.group_box_layout.addLayout(bullet)
            if self.first_box_index == None:
                self.first_box_index = self.boxes_layout.indexOf(box)
            self.line_edit.setText("")

    # when button is clicked, show the checkboxes next to the bullet points
    def remove_was_clicked(self):
        if self.remove_button.isChecked():
            self.toggle_all_checkboxes()
            self.enter_button.setDisabled(True)
            self.edit_button.setDisabled(True)
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
        for bullet in self.group_box.findChildren(bulletPoint.BulletPoint):
            if checkboxFunctions.is_checked(checkboxFunctions.get_checkbox(bullet)):
                return True
        return False

    # change back to state before remove mode was enabled
    def revert_remove_mode(self):
        self.remove_button.setChecked(False)
        self.toggle_all_checkboxes()
        self.uncheck_all()
        self.enter_button.setDisabled(False)
        self.edit_button.setDisabled(False)

    def toggle_all_checkboxes(self):
        for bullet in self.group_box.findChildren(bulletPoint.BulletPoint):
            checkboxFunctions.toggle_checkbox_visible(checkboxFunctions.get_checkbox(bullet))

    def uncheck_all(self):
        for bullet in self.group_box.findChildren(bulletPoint.BulletPoint):
            if checkboxFunctions.is_checked(checkboxFunctions.get_checkbox(bullet)):
                bullet.uncheck()

    def on_delete_ok(self):
        for bullet in self.group_box.findChildren(bulletPoint.BulletPoint):
            if checkboxFunctions.is_checked(checkboxFunctions.get_checkbox(bullet)):
                box = self.find_matching_box(bullet.get_text())
                if box != None:
                    self.main_layout.removeWidget(box)
                    bullet.remove_items()
                    self.group_box_layout.removeItem(bullet)
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
        cond = lambda bool: not bool if self.toggle_boxes_button.isChecked() else bool
        setTxt = lambda: "Collapse All" if self.toggle_boxes_button.isChecked() else "Expand All"
        self.toggle_boxes_button.setText(setTxt())
        for i in range(self.boxes_layout.count()):
            item = self.boxes_layout.itemAt(i).widget()
            if isinstance(item, collapsableBox.CollapsableBox) and cond(item.get_checked()):
                item.toggle_checked()
                item.button_was_clicked()

    def is_duplicate_bullet(self, text):
        for bullet in self.group_box.findChildren(bulletPoint.BulletPoint):
            if bullet.get_text() == text:
                return True
        return False

    def on_enter_edit_ok(self):
        edit = editWindow.EditWindow(self.group_box.findChildren(bulletPoint.BulletPoint))
        dlg = customDialog.CustomDialog(
            self, "Edit", QSize(400, 700), edit, self.on_edit_ok, self.on_edit_reject
        )
        dlg.exec()

    def on_edit_reject(self):
        self.line_edit.clear()

    def on_edit_ok(self, widget):
        # Change bulletpoint buttons texts
        bullet_points = self.group_box.findChildren(bulletPoint.BulletPoint)
        line_edits = widget.sorted_children()
        for (bullet, line_edit) in zip(bullet_points, line_edits):
            bullet.set_text(line_edit.text())

        # Change the box texts
        for i in range(len(line_edits)):
            target_index = self.first_box_index + i
            box = self.find_matching_box(line_edits[i].text())
            index_of_box = self.boxes_layout.indexOf(box)
            if index_of_box != target_index:
                temp = self.boxes_layout.itemAt(target_index).widget()
                temp_title = temp.text()
                temp_text = temp.get_written_work()

                temp.set_text(box.text())
                temp.set_writing(box.get_written_work())

                box.set_text(temp_title)
                box.set_writing(temp_text)

    def on_to_top(self):
        self.scroll.ensureWidgetVisible(self.outline_label)

    def get_all_text(self):
        text = ""
        for i in range(self.boxes_layout.count()):
            item = self.boxes_layout.itemAt(i).widget()
            if item != None:
                text += "\n" + item.get_written_work()
        return text

    def get_current_box(self):
        for i in range(self.boxes_layout.count()):
            item = self.boxes_layout.itemAt(i).widget()
            if item != None and item.text_edit.hasFocus():
                return item
        return None

    def on_placeholder_requested(self):
        if self.first_box_index != None:
            first_box = self.boxes_layout.itemAt(self.first_box_index)
            if first_box != None:
                cur_box = self.get_current_box()
                pos = QCursor.pos()
                self.placeholders.show_menu(self.clamp(pos, self.geometry().topLeft(), self.geometry().bottomRight()), cur_box)

    def clamp(self, pos, smallest, greatest):
        x = max(smallest.x(), min(pos.x(), greatest.x()))
        y = max(smallest.y(), min(pos.y(), greatest.y()))
        return QPoint(x, y)

    def on_placeholders_manage(self):
        self.placeholders.set_add_new(False)
        self.placeholders.popup(QCursor.pos())
        # MAke sure pressing the things won't do anything


class PlaceHolderMechanism(QMenu):
    def __init__(self, parent):
        super().__init__()
        self.setTitle("Placeholders")
        self.parent = parent
        self.add_new_action = QAction("Add new")
        self.add_new_action.triggered.connect(self.add_new)
        self.addAction(self.add_new_action)

        self.placeholders = {}
        self.cur_box = None

    def show_menu(self, pos, cur_box):
        self.cur_box = cur_box
        self.popup(pos)

    def add_new(self):
        dlg = customDialog.CustomDialog(
            self, "Add New Placeholder", QSize(200, 100), QLineEdit(), self.on_add_ok, None
        )
        dlg.exec()

    def on_add_ok(self, widget):
        dlg = QColorDialog()
        color = dlg.getColor()
        self.placeholders[widget.text()] = [color, []]
        self.addAction(widget.text())
        self.add_to_existing(widget.text())

    def add_to_existing(self, key):
        cur_point = self.parent.mapToGlobal(self.cur_box.geometry().topLeft())
        self.placeholders[key][1].append(cur_point)

        self.cur_box.set_text_color(self.placeholders[key][0])
        self.cur_box.append_text(key)
        self.cur_box.set_text_color(QColor(0, 0, 0))

    def triggered(self, action):
        print("action text is ", action.text())
        if action.text() != "Add new":
            if not self.add_new_action.isEnabled():
                self.on_show_placeholders_positions(action)
            else:
                self.add_to_existing(action.text())

    def set_add_new(self, enabled):
        self.add_new_action.setEnabled(enabled)

    def on_show_placeholders_positions(self, action):
        self.set_add_new(True)
