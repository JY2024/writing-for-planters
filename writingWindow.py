import os

from PyQt5 import QtCore
from PyQt5.QtGui import QKeySequence, QCursor, QColor, QTextDocument

import boxForStory
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
    QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QGroupBox, QShortcut, QMenu,
    QColorDialog, QAction
)


# Writing window
class WritingWindow(scrollableWindow.ScrollableWindow):
    def __init__(self, title, path):
        self.path = path
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
        self.local_save_button = designFunctions.generate_button("Local &Save")
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
        self.main_layout.addWidget(self.local_save_button)
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

        super().__init__(title, QSize(1000, 800), self.main_layout)

        self.placeholders = PlaceHolderMechanism(self)

        # Connect signals
        self.enter_button.clicked.connect(self.enter_was_clicked)
        self.remove_button.clicked.connect(self.remove_was_clicked)
        self.toggle_boxes_button.clicked.connect(self.toggle_boxes_clicked)
        self.edit_button.clicked.connect(self.on_enter_edit_ok)
        self.placeholders_button.clicked.connect(self.on_placeholders_manage)
        self.local_save_button.clicked.connect(self.on_local_save)

        # Shortcuts
        to_top_shortcut = QShortcut(QKeySequence(self.tr("Ctrl+O")), self)
        to_top_shortcut.activated.connect(self.on_to_top)
        placeholder_shortcut = QShortcut(QKeySequence(self.tr("Ctrl+H")), self)
        placeholder_shortcut.activated.connect(self.on_placeholder_requested)
        italics_shortcut = QShortcut(QKeySequence(self.tr("Ctrl+I")), self)
        italics_shortcut.activated.connect(self.on_italics)
        save_shortcut = QShortcut(QKeySequence(self.tr("Ctrl+S")), self)
        save_shortcut.activated.connect(self.on_local_save)

        self.first_box_index = None

    # when button is clicked, place text into outline group of buttons
    def enter_was_clicked(self):
        text = self.line_edit.text()
        if self.is_duplicate_bullet(text):
            dlg = customDialog.CustomDialog(
                self, "Duplicate Bulletpoint", QSize(300, 100),
                QLabel("You already have a bulletpoint with this name.\nDo you want to reorder instead?"),
                self.on_enter_edit_ok, self.on_edit_reject
            )
            dlg.exec()
        else:
            self.num_parts += 1
            box = boxForStory.BoxForStory(text, self.num_parts)
            self.boxes_layout.addWidget(box)
            bullet = bulletPoint.BulletPoint(text, self, box, self.num_parts)
            self.group_box_layout.addLayout(bullet)
            if self.first_box_index == None:
                self.first_box_index = self.boxes_layout.indexOf(box)
            self.line_edit.setText("")

            box_file = open(os.path.join(self.path, "box" + box.text() + ".txt"), "w+")
            box_str = "_BUTTON_" + box.text() + "_BUTTON_TEXT_" + box.to_html() + "_TEXT_COMMENTS_" + box.comments() + "_COMMENTS_"
            box_file.write(box_str)
            box_file.close()

    # when button is clicked, show the checkboxes next to the bullet points
    def remove_was_clicked(self):
        if self.remove_button.isChecked():
            self.toggle_all_checkboxes()
            self.enter_button.setDisabled(True)
            self.edit_button.setDisabled(True)
        else:
            if self.at_least_one_checked():
                dlg = customDialog.CustomDialog(
                    self, "Deletion", QSize(300, 100),
                    QLabel("Are you sure you want to delete this?\nTHIS IS NOT REVERSIBLE"), self.on_delete_ok,
                    self.revert_remove_mode
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
                    # Remove from directory
                    if os.path.exists(os.path.join(self.path, "box" + box.text() + ".txt")):
                        os.remove(os.path.join(self.path, "box" + box.text() + ".txt"))
                    self.boxes_layout.removeWidget(box)
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
        self.scroll.ensureWidgetVisible(self.local_save_button)

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
            if item != None and (item.text_edit.hasFocus() or item.comment_text_edit.hasFocus()):
                return item
        return None

    def on_placeholder_requested(self):
        if self.first_box_index != None:
            first_box = self.boxes_layout.itemAt(self.first_box_index)
            if first_box != None:
                cur_box = self.get_current_box()
                pos = QCursor.pos()
                self.placeholders.show_menu(self.clamp(pos, self.geometry().topLeft(), self.geometry().bottomRight()),
                                            cur_box)

    def clamp(self, pos, smallest, greatest):
        return QPoint(self.clamp_int(pos.x(), smallest.x(), greatest.x()),
                      self.clamp_int(pos.y(), smallest.y(), greatest.y()))

    def clamp_int(self, n, smallest, greatest):
        return max(smallest, min(n, greatest))

    def on_placeholders_manage(self):
        if self.first_box_index != None and self.boxes_layout.itemAt(self.first_box_index) != None:
            self.placeholders.show_menu(QCursor.pos(), self.get_current_box())

    def on_italics(self):
        self.get_current_box().toggle_italics()

    def get_all_boxes(self):
        boxes = []
        for i in range(self.boxes_layout.count()):
            item = self.boxes_layout.itemAt(i).widget()
            if isinstance(item, collapsableBox.CollapsableBox):
                boxes.append(item)
        return boxes

    def get_path(self):
        return self.path

    def add_box(self, header_text, box_text, comment_text):
        self.num_parts += 1
        box = boxForStory.BoxForStory(header_text, self.num_parts)
        box.load_text(box_text, comment_text)
        self.boxes_layout.addWidget(box)
        bullet = bulletPoint.BulletPoint(header_text, self, box, self.num_parts)
        self.group_box_layout.addLayout(bullet)
        if self.first_box_index == None:
            self.first_box_index = self.boxes_layout.indexOf(box)
        self.line_edit.setText("")

    def on_local_save(self):
        # Save placeholders
        placeholders_str = self.placeholders.get_placeholders_string()
        holders_file = open(os.path.join(self.path, "placeholders.txt"), "w+")
        holders_file.write(placeholders_str)
        holders_file.close()
        # Save boxes and buttons
        boxes = self.get_all_boxes()
        for box in boxes:
            box_file = open(os.path.join(self.path, "box" + box.text() + ".txt"), "w+")
            box_str = "_BUTTON_" + box.text() + "_BUTTON_TEXT_" + box.to_html() + "_TEXT_COMMENTS_" + box.comments() + "_COMMENTS_"
            box_file.write(box_str)
            box_file.close()

    def add_placeholders(self, placeholder_names, colors):
        for (name, color) in zip(placeholder_names, colors):
            self.placeholders.add_placeholder(name, QColor.fromRgb(int(color)))

class PlaceHolderMechanism(QMenu):
    def __init__(self, parent):
        super().__init__(parent)
        self.setTitle("Placeholders")
        self.parent = parent
        self.add_new_action = QAction("Add new")
        self.add_new_action.triggered.connect(self.triggered)
        self.addAction(self.add_new_action)

        self.placeholders = {}
        self.cur_box = None

        self.window = None

    def get_placeholders_string(self):
        string = ""
        for holder_name in self.placeholders.keys():
            string += "_HOLDER_" + holder_name + ";" + str(self.placeholders[holder_name].rgb()) + "_HOLDER_"
        return string

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

        self.add_placeholder(widget.text(), color)

        if self.cur_box != None and (self.cur_box.text_edit.hasFocus() or self.cur_box.comment_text_edit.hasFocus()):
            self.add_to_existing(widget.text())

    def add_to_existing(self, key):
        self.cur_box = self.parent.get_current_box()
        self.cur_box.set_text_color(self.placeholders[key])
        self.cur_box.append_text(key)
        self.cur_box.set_text_color(QColor(0, 0, 0))

    def triggered(self):
        action = self.sender()
        if action.text() == "Add new":
            self.add_new()
        else:
            if self.cur_box != None and (
                    self.cur_box.text_edit.hasFocus() or self.cur_box.comment_text_edit.hasFocus()):
                self.add_to_existing(action.text())
            else:
                self.on_show_placeholders_positions(action)

    def on_show_placeholders_positions(self, action):
        self.window = PlaceholderSummaryDisplay(self.parent, action.text())
        self.window.show()

    def add_placeholder(self, text, color):
        self.placeholders[text] = color
        self.addAction(text, self.triggered)


class PlaceholderSummaryDisplay(scrollableWindow.ScrollableWindow):
    def __init__(self, parent, action_name):
        self.parent = parent
        self.action_name = action_name

        self.layout = QVBoxLayout()
        self.set_up()

        super().__init__(action_name + " Placeholders Summary", QSize(800, 500), self.layout)

    def set_up(self):
        for i in range(self.parent.boxes_layout.count()):
            item = self.parent.boxes_layout.itemAt(i).widget()
            if isinstance(item, collapsableBox.CollapsableBox) and item.has_placeholder(self.action_name):
                self.layout.addWidget(QLabel(item.text()))
                label = designFunctions.generate_textEdit(
                    doc=QTextDocument(self.extract_text_excerpts(item.get_written_work())),
                    background_color="white", size=QSize(600, 400), read_only=True)
                self.layout.addWidget(label)

    def extract_text_excerpts(self, text):
        text = " ".join(text.split())
        excerpt_text = ""
        substring = text[0:]
        prev_accumulated = 0
        while len(substring) > 0 and (self.action_name in substring):
            index = substring.index(self.action_name) + prev_accumulated
            start = self.parent.clamp_int(index - 30, 0, len(text))
            end = self.parent.clamp_int(index + len(self.action_name) + 30, 0, len(text))

            str = text[start:end]
            str = str.replace(self.action_name, self.action_name.upper())
            start_str = "\"" if start == 0 else "\"..."
            end_str = "\"\n\n" if end == len(text) else "...\"\n\n"
            excerpt_text += start_str + str + end_str

            substring = substring[substring.index(self.action_name) + len(self.action_name):]
            prev_accumulated = (index + len(self.action_name))
        return excerpt_text
