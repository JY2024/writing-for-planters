import os

from PyQt5.QtCore import QPoint, QSize
from PyQt5.QtGui import QColor, QCursor, QKeySequence, QTextDocument
from PyQt5.QtWidgets import (
    QAction, QColorDialog, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QMenu, QShortcut, QStyle, QVBoxLayout
)

import boxForStory
import bulletPoint
import checkboxFunctions
import collapsableBox
import customDialog
import designFunctions
import editWindow
import scrollableWindow


class WritingWindow(scrollableWindow.ScrollableWindow):
    """ScrollableWindow for writing one part of a work, with BulletPoints and CollapsableBoxes"""
    def __init__(self, parent, title, path):
        self.parent = parent
        self.path = path
        self.num_parts = 0
        self.first_box_index = None

        self.line_edit = QLineEdit()
        self.group_box = QGroupBox()
        self.group_box_layout = QVBoxLayout()
        self.box_for_boxes = QGroupBox()
        self.boxes_layout = QVBoxLayout()

        self.back_button = designFunctions.generate_button(background_color="light grey", size=QSize(30, 30))
        self.local_save_button = designFunctions.generate_button("Local &Save")
        self.enter_button = designFunctions.generate_button("&Enter", checkable=False)
        self.remove_button = designFunctions.generate_button("Remove", checkable=True)
        self.toggle_boxes_button = designFunctions.generate_button("Expand All", checkable=True)
        self.edit_button = designFunctions.generate_button("Edit", checkable=False)
        self.placeholders_button = designFunctions.generate_button("Manage Placeholders")

        self.main_layout = QVBoxLayout()
        self.below_story_layout = QHBoxLayout()

        super().__init__(title, QSize(1000, 800), self.main_layout)
        self.placeholders = PlaceHolderMechanism(self)
        self.init_ui()

    def init_ui(self):
        """Initializes UI for WritingWindow"""
        self.box_for_boxes.setLayout(self.boxes_layout)
        story_label = designFunctions.generate_label("Story", bold=True, font_size="20px")
        outline_label = designFunctions.generate_label("Outline", bold=True, font_size="20px")

        self.line_edit.setMaximumSize(QSize(500, 100))
        self.line_edit.setStyleSheet("background-color: rgb(243,240,240)")
        self.group_box.setStyleSheet("background-color: rgb(243,240,240)")
        self.group_box.setLayout(self.group_box_layout)
        self.group_box.setMaximumSize(QSize(500, 500))

        self.main_layout.addWidget(self.back_button)
        self.main_layout.addWidget(self.local_save_button)
        self.main_layout.addWidget(outline_label)
        outline_layout = QHBoxLayout()
        outline_layout.addWidget(self.line_edit)
        outline_layout.addWidget(self.group_box)
        self.main_layout.addLayout(outline_layout)
        self.main_layout.addWidget(self.enter_button)
        self.main_layout.addWidget(self.remove_button)
        self.main_layout.addWidget(self.edit_button)
        self.main_layout.addWidget(story_label)
        self.below_story_layout.addWidget(self.toggle_boxes_button)
        self.below_story_layout.addWidget(self.placeholders_button)
        self.main_layout.addLayout(self.below_story_layout)
        self.main_layout.addWidget(self.box_for_boxes)

        pixmapi = getattr(QStyle, "SP_ArrowBack")
        icon = self.style().standardIcon(pixmapi)
        self.back_button.setIcon(icon)

        self.enter_button.clicked.connect(self.enter_was_clicked)
        self.remove_button.clicked.connect(self.remove_was_clicked)
        self.toggle_boxes_button.clicked.connect(self.toggle_boxes_clicked)
        self.edit_button.clicked.connect(self.on_enter_edit_ok)
        self.placeholders_button.clicked.connect(self.on_placeholders_manage)
        self.local_save_button.clicked.connect(self.on_local_save)
        self.back_button.clicked.connect(self.on_back)

        to_top_shortcut = QShortcut(QKeySequence(self.tr("Ctrl+O")), self)
        to_top_shortcut.activated.connect(self.on_to_top)
        placeholder_shortcut = QShortcut(QKeySequence(self.tr("Ctrl+H")), self)
        placeholder_shortcut.activated.connect(self.on_placeholder_requested)
        italics_shortcut = QShortcut(QKeySequence(self.tr("Ctrl+I")), self)
        italics_shortcut.activated.connect(self.on_italics)
        save_shortcut = QShortcut(QKeySequence(self.tr("Ctrl+S")), self)
        save_shortcut.activated.connect(self.on_local_save)

    def at_least_one_checked(self):
        """Returns whether at least one BulletPoint is checked"""
        for bullet in self.group_box.findChildren(bulletPoint.BulletPoint):
            if checkboxFunctions.is_checked(checkboxFunctions.get_checkbox(bullet)):
                return True
        return False

    def revert_remove_mode(self):
        """Reverts state to before remove mode was enabled"""
        self.remove_button.setChecked(False)
        self.toggle_all_checkboxes()
        self.uncheck_all()
        self.enter_button.setDisabled(False)
        self.edit_button.setDisabled(False)

    def toggle_all_checkboxes(self):
        """Toggles checkboxes checked state of all BulletPoints"""
        for bullet in self.group_box.findChildren(bulletPoint.BulletPoint):
            checkboxFunctions.toggle_checkbox_visible(checkboxFunctions.get_checkbox(bullet))

    def uncheck_all(self):
        """Unchecks all BulletPoints"""
        for bullet in self.group_box.findChildren(bulletPoint.BulletPoint):
            if checkboxFunctions.is_checked(checkboxFunctions.get_checkbox(bullet)):
                bullet.uncheck()

    def find_matching_box(self, text):
        """Takes text: string, returns the BoxForStory with the given button text"""
        for i in range(self.boxes_layout.count()):
            item = self.boxes_layout.itemAt(i).widget()
            if item != None and item.get_button_text() == text:
                return item
        return None

    def toggle_boxes_clicked(self):
        """Handles expanding and collapsing the correct CollapsableBoxes based on whether they need to collapse or
        expand"""
        # Whether cond needs to be true depends on whether boxes need to be collapsed or expanded
        cond = lambda bool: not bool if self.toggle_boxes_button.isChecked() else bool
        setTxt = lambda: "Collapse All" if self.toggle_boxes_button.isChecked() else "Expand All"
        self.toggle_boxes_button.setText(setTxt())
        for i in range(self.boxes_layout.count()):
            item = self.boxes_layout.itemAt(i).widget()
            if isinstance(item, collapsableBox.CollapsableBox) and cond(item.get_checked()):
                item.toggle_checked()
                item.on_text_button_clicked()

    def is_duplicate_bullet(self, text):
        """Takes text: string, returns whether an existing BulletPoint already has the same text"""
        for bullet in self.group_box.findChildren(bulletPoint.BulletPoint):
            if bullet.get_text() == text:
                return True
        return False

    def clamp(self, pos, smallest, greatest):
        """Takes pos: QPoint, smallest: QPoint, greatest: QPoint, returns QPoint with clamped values"""
        return QPoint(self.clamp_int(pos.x(), smallest.x(), greatest.x()),
                      self.clamp_int(pos.y(), smallest.y(), greatest.y()))

    def clamp_int(self, n, smallest, greatest):
        """Takes n: int, smallest: int, greatest: int, returns int clamped between smallest and greatest"""
        return max(smallest, min(n, greatest))

    def add_box(self, header_text, box_text, comment_text):
        """Takes header_text: string, box_text: string, comment_text: string, adds CollapsableBox to window"""
        self.num_parts += 1
        box = boxForStory.BoxForStory(header_text, self.num_parts)
        box.load_text(box_text, comment_text)
        self.boxes_layout.addWidget(box)
        bullet = bulletPoint.BulletPoint(header_text, self, box, self.num_parts)
        self.group_box_layout.addLayout(bullet)
        if self.first_box_index == None:
            self.first_box_index = self.boxes_layout.indexOf(box)
        self.line_edit.setText("")

    def add_placeholders(self, placeholder_names, colors):
        """Takes placeholder_names: string[], colors: QColor[], adds placeholders with matching name and QColor pairs"""
        for (name, color) in zip(placeholder_names, colors):
            self.placeholders.add_placeholder(name, QColor.fromRgb(int(color)))

    def on_back(self):
        """Handles back button click, closes this window and opens corresponding WorkPage"""
        self.parent.show()
        self.close()

    def enter_was_clicked(self):
        """Handles enter button clicked event, places text into outline group of BulletPoints and adds CollapsableBox"""
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
            box_file = open(os.path.join(self.path, "box" + box.get_button_text() + ".txt"), "w+")
            box_str = "_BUTTON_" + box.get_button_text() + "_BUTTON_TEXT_" + box.to_html() + "_TEXT_COMMENTS_" + box.get_comments() + "_COMMENTS_"
            box_file.write(box_str)
            box_file.close()

    def remove_was_clicked(self):
        """Handles remove button clicked event, toggles checkboxes of BulletPoints or prompts user to confirm removal"""
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

    def on_delete_ok(self):
        """Deletes all checked BulletPoints and their corresponding CollapsableBoxes"""
        for bullet in self.group_box.findChildren(bulletPoint.BulletPoint):
            if checkboxFunctions.is_checked(checkboxFunctions.get_checkbox(bullet)):
                box = self.find_matching_box(bullet.get_text())
                if box != None:
                    # Remove from directory
                    if os.path.exists(os.path.join(self.path, "box" + box.get_button_text() + ".txt")):
                        os.remove(os.path.join(self.path, "box" + box.get_button_text() + ".txt"))
                    self.boxes_layout.removeWidget(box)
                    bullet.remove_items()
                    self.group_box_layout.removeItem(bullet)
        self.revert_remove_mode()

    def bulletPoint_was_clicked(self, bullet):
        """Takes bullet: BulletPoint, handles BulletPoint clicked event by jumping view to matching CollapsableBox"""
        box = self.find_matching_box(bullet.get_text())
        self.scroll.ensureWidgetVisible(box)

    def on_enter_edit_ok(self):
        """Displays window for editing/reordering BulletPoints and CollapsableBoxes"""
        edit = editWindow.EditWindow(self.group_box.findChildren(bulletPoint.BulletPoint))
        dlg = customDialog.CustomDialog(
            self, "Edit", QSize(400, 700), edit, self.on_edit_ok, self.on_edit_reject
        )
        dlg.exec()

    def on_edit_reject(self):
        """Handles edit rejection by clearing the LineEdit"""
        self.line_edit.clear()

    def on_edit_ok(self, widget):
        """Takes widget: EditWindow, Changes the BulletPoint order and CollapsableBox order to match the desired order"""
        bullet_points = self.group_box.findChildren(bulletPoint.BulletPoint)
        line_edits = widget.sorted_children()
        for (bullet, line_edit) in zip(bullet_points, line_edits):
            bullet.set_button_text(line_edit.text())

        for i in range(len(line_edits)):
            target_index = self.first_box_index + i
            box = self.find_matching_box(line_edits[i].text())
            index_of_box = self.boxes_layout.indexOf(box)
            if index_of_box != target_index:
                temp = self.boxes_layout.itemAt(target_index).widget()
                temp_title = temp.get_button_text()
                temp_text = temp.get_written_work()
                temp_comment = temp.get_comment()

                temp.set_button_text(box.get_button_text())
                temp.set_writing(box.get_written_work())
                temp.set_comment(box.get_comment())

                box.set_button_text(temp_title)
                box.set_writing(temp_text)
                box.set_comment(temp_comment)

    def on_to_top(self):
        """Handles to top request, ensures the top is visible"""
        self.scroll.ensureWidgetVisible(self.back_button)

    def on_placeholder_requested(self):
        """Handles placeholder request, opens placeholder menu"""
        if self.first_box_index != None:
            first_box = self.boxes_layout.itemAt(self.first_box_index)
            if first_box != None:
                cur_box = self.get_current_box()
                pos = QCursor.pos()
                self.placeholders.show_menu(self.clamp(pos, self.geometry().topLeft(), self.geometry().bottomRight()),
                                            cur_box)

    def on_placeholders_manage(self):
        """Handles Manage Placeholders button clicked event, displays menu"""
        if self.first_box_index != None and self.boxes_layout.itemAt(self.first_box_index) != None:
            self.placeholders.show_menu(QCursor.pos(), self.get_current_box())

    def on_italics(self):
        """Toggles italics on or off for the current CollapsableBox"""
        self.get_current_box().toggle_italics()

    def on_local_save(self):
        """Handles local save request, saves all text"""
        # Save placeholders
        placeholders_str = self.placeholders.get_placeholders_string()
        holders_file = open(os.path.join(self.path, "placeholders.txt"), "w+")
        holders_file.write(placeholders_str)
        holders_file.close()
        # Save boxes and buttons
        boxes = self.get_all_boxes()
        box_order = []
        for box in boxes:
            box_order.append(box.get_button_text())
            box_file = open(os.path.join(self.path, "box" + box.get_button_text() + ".txt"), "w+")
            box_str = "_BUTTON_" + box.get_button_text() + "_BUTTON_TEXT_" + box.to_html() + "_TEXT_COMMENTS_" + box.get_comments() + "_COMMENTS_"
            box_file.write(box_str)
            box_file.close()

        box_order_file = open(os.path.join(self.path, "box_order.txt"), "w+")
        for box_name in box_order:
            box_order_file.write(box_name + ";")
        box_order_file.close()

    def get_all_text(self):
        """Returns all text in this part"""
        text = ""
        for i in range(self.boxes_layout.count()):
            item = self.boxes_layout.itemAt(i).widget()
            if item != None:
                text += "\n" + item.get_written_work()
        return text

    def get_current_box(self):
        """Returns the CollapsableBox that currently has the user's input focus"""
        for i in range(self.boxes_layout.count()):
            item = self.boxes_layout.itemAt(i).widget()
            if item != None and (item.text_edit.hasFocus() or item.comment_text_edit.hasFocus()):
                return item
        return None

    def get_all_boxes(self):
        """Returns all CollapsableBoxes in array"""
        boxes = []
        for i in range(self.boxes_layout.count()):
            item = self.boxes_layout.itemAt(i).widget()
            if isinstance(item, collapsableBox.CollapsableBox):
                boxes.append(item)
        return boxes

    def get_path(self):
        """Returns path: string"""
        return self.path


class PlaceHolderMechanism(QMenu):
    """Menu or mechanism for storing placeholders and its functions"""
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.placeholders = {}
        self.cur_box = None
        self.window = None

        self.setTitle("Placeholders")
        self.add_new_action = QAction("Add new")
        self.add_new_action.triggered.connect(self.triggered)
        self.addAction(self.add_new_action)

    def show_menu(self, pos, cur_box):
        """Takes pos: QPoint, cur_box: CollapsableBox, shows menu at indicated position"""
        self.cur_box = cur_box
        self.popup(pos)

    def add_new(self):
        """Displays dialog for adding a new placeholder"""
        dlg = customDialog.CustomDialog(
            self, "Add New Placeholder", QSize(200, 100), QLineEdit(), self.on_add_ok, None
        )
        dlg.exec()

    def on_add_ok(self, widget):
        """Takes widget: QLineEdit, adds new placeholder"""
        dlg = QColorDialog()
        color = dlg.getColor()
        self.add_placeholder(widget.text(), color)
        if self.cur_box != None and (self.cur_box.text_edit.hasFocus() or self.cur_box.comment_text_edit.hasFocus()):
            self.add_to_existing(widget.text())

    def add_to_existing(self, key):
        """Takes key: string, adds placeholder to the current CollapsableBox"""
        self.cur_box = self.parent.get_current_box()
        self.cur_box.set_text_color(self.placeholders[key])
        self.cur_box.append_text(key)
        self.cur_box.set_text_color(QColor(0, 0, 0))

    def triggered(self):
        """Handles selection from placeholder menu"""
        action = self.sender()
        if action.text() == "Add new":
            self.add_new()
        else:
            if self.cur_box != None and (self.cur_box.text_edit.hasFocus() or self.cur_box.comment_text_edit.hasFocus()):
                self.add_to_existing(action.text())
            else:
                self.on_show_placeholders_positions(action)

    def on_show_placeholders_positions(self, action):
        """Takes action: QEvent, Displays window showing PlaceHolderSummary for requested placeholder"""
        self.window = PlaceholderSummaryDisplay(self.parent, action.text())
        self.window.show()

    def add_placeholder(self, text, color):
        """Takes text: string, color: QColor, adds placeholder"""
        self.placeholders[text] = color
        self.addAction(text, self.triggered)

    def get_placeholders_string(self):
        """Returns all placeholders in a string with pairs in a name;color_name format"""
        string = ""
        for holder_name in self.placeholders.keys():
            string += "_HOLDER_" + holder_name + ";" + str(self.placeholders[holder_name].rgb()) + "_HOLDER_"
        return string


class PlaceholderSummaryDisplay(scrollableWindow.ScrollableWindow):
    """ScrollableWindow that displays occurrences of placeholder name within this WritingWindow"""
    def __init__(self, parent, action_name):
        self.parent = parent
        self.action_name = action_name
        self.layout = QVBoxLayout()
        self.init_ui()

        super().__init__(action_name + " Placeholders Summary", QSize(800, 500), self.layout)

    def init_ui(self):
        """Initializes UI for PlaceholderSummaryDisplay"""
        for i in range(self.parent.boxes_layout.count()):
            item = self.parent.boxes_layout.itemAt(i).widget()
            if isinstance(item, collapsableBox.CollapsableBox) and item.has_placeholder(self.action_name):
                self.layout.addWidget(QLabel(item.get_button_text()))
                label = designFunctions.generate_textEdit( # New label with text excerpts containing the placeholder
                    doc=QTextDocument(self.extract_text_excerpts(item.get_written_work())),
                    background_color="white", size=QSize(600, 400), read_only=True)
                self.layout.addWidget(label)

    def extract_text_excerpts(self, text):
        """Takes text: string, returns text excerpts of all parts in CollapsableBoxes that have the placeholder"""
        text = " ".join(text.split())
        excerpt_text = ""
        substring = text[0:] # Substring from text that is currently being examined for occurrences of placeholder
        prev_accumulated = 0 # Accumulated "distance" through the text string so far
        while len(substring) > 0 and (self.action_name in substring):
            index = substring.index(self.action_name) + prev_accumulated
            start = self.parent.clamp_int(index - 30, 0, len(text)) # Start of excerpt, to the left of placeholder
            end = self.parent.clamp_int(index + len(self.action_name) + 30, 0, len(text)) # End of excerpt, to the right

            str = text[start:end]
            str = str.replace(self.action_name, self.action_name.upper())
            start_str = "\"" if start == 0 else "\"..."
            end_str = "\"\n\n" if end == len(text) else "...\"\n\n"
            excerpt_text += start_str + str + end_str

            substring = substring[substring.index(self.action_name) + len(self.action_name):]
            prev_accumulated = (index + len(self.action_name))
        return excerpt_text