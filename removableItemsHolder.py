import os
import shutil

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QLabel, QFileDialog

import customDialog
import workCreationWidget
import checkboxFunctions

class RemovableItemsHolder(QGroupBox):
    def __init__(self, parent, create_button, remove_button, part_creation_widget, part_summary, part, path):
        super().__init__()
        self.parent = parent
        self.path = path
        self.part_creation_widget = part_creation_widget
        self.part_summary = part_summary
        self.part = part
        self.remove_button = remove_button
        self.create_button = create_button
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.setLayout(self.main_layout)
        self.parts = {}

    def on_create_clicked(self):
        helper_widget = self.part_creation_widget if isinstance(self.part_creation_widget, QLabel) else self.part_creation_widget()
        dlg = customDialog.CustomDialog(
            self, "Create", QSize(500, 500), helper_widget, self.on_create_ok, None
        )
        dlg.exec()

    def on_create_ok(self, widget):
        my_part_summary = None
        my_part = None
        if len(self.parts.keys()) == 0 or widget.get_title() not in self.parts:
            if isinstance(widget, workCreationWidget.WorkCreationWidget):
                # For creating a work summary in works window
                cur_path = QFileDialog.getExistingDirectory(parent=self, caption="Select Directory",
                                                            options=QFileDialog.ShowDirsOnly)  # Path to new folder
                if cur_path != "":
                    my_part = self.part(self.parent, widget.get_title(), widget.get_tags(), widget.get_description(), cur_path)
                    my_part_summary = self.part_summary(self.parent, self, widget.get_title(), widget.get_tags(), widget.get_description(), my_part)

                    # Save title, description, and tags
                    work_summary_file = open(os.path.join(cur_path, "summary.txt"), "w+")
                    summary_string = "_TITLE_" + widget.get_title() + "_TITLE_TAGS_" + widget.get_tags().toPlainText() \
                                 + "_TAGS_DESCRIPTION_" + widget.get_description().toPlainText() + "_DESCRIPTION_"
                    work_summary_file.write(summary_string)
                    work_summary_file.close()
            else:
                # New directory
                dir_path = os.path.join(self.path, "part" + widget.get_title() + ".dir")
                os.mkdir(dir_path)
                # For creating a part summary in a work page
                my_part_summary = self.part_summary(self.parent, self, widget.get_title(), widget.get_description())
                my_part = self.part(self.parent, widget.get_title(), dir_path)
                # Save part title and synopsis
                part_header_file = open(os.path.join(dir_path, "header.txt"), "w+")
                part_header_string = "_TITLE_" + widget.get_title() + "_TITLE_SYNOPSIS_" + widget.get_description().toPlainText() + "_SYNOPSIS_"
                part_header_file.write(part_header_string)
                part_header_file.close()
                # Placeholders
                placeholders_file = open(os.path.join(dir_path, "placeholders.txt"), "w+")
                placeholders_file.write("_HOLDERS__HOLDERS_")
                placeholders_file.close()
                # Box order
                box_order_file = open(os.path.join(dir_path, "box_order.txt"), "w+")
                box_order_file.write("")
                box_order_file.close()
            self.main_layout.addWidget(my_part_summary)
            self.parts[widget.get_title()] = [my_part_summary, my_part]

    def toggle_all_checkboxes(self):
        for key in self.parts.keys():
            check_box = checkboxFunctions.get_checkbox(self.parts[key][0])
            check_box.setChecked(False)
            checkboxFunctions.toggle_checkbox_visible(check_box)

    def open_part(self, title):
        self.parts[title][1].show()

    def on_remove_clicked(self):
        if self.remove_button.isChecked():
            self.create_button.setDisabled(True)
            self.toggle_all_checkboxes()
        else:
            self.create_button.setDisabled(False)
            dlg = customDialog.CustomDialog(
                self, "Remove", QSize(300, 100),
                QLabel("Are you sure you want to remove these?\nTHIS IS NOT REVERSIBLE."), self.on_remove_ok,
                self.toggle_all_checkboxes
            )
            dlg.exec()

    def on_remove_ok(self):
        for title in list(self.parts):
            summary = self.parts[title][0]
            if checkboxFunctions.is_checked(checkboxFunctions.get_checkbox(summary)):
                path = self.parts[title][1].get_path()
                if os.path.exists(path):
                    shutil.rmtree(path)
                self.main_layout.removeWidget(summary)
                self.parts.pop(title)
        self.toggle_all_checkboxes()

    def get_parts(self):
        return self.parts

    def add_part(self, title, summary, part):
        self.parts[title] = [summary, part]

    def add_widget(self, widget):
        self.main_layout.addWidget(widget)



