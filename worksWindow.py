import os
import pathlib

from PyQt5.QtCore import QSize

import designFunctions
import removableItemsHolder
import workCreationWidget
import workSummary
import workPage
import scrollableWindow
from PyQt5.QtWidgets import QVBoxLayout, QFileDialog, QMessageBox


class WorksWindow(scrollableWindow.ScrollableWindow):
    def __init__(self):
        self.layout = QVBoxLayout()
        self.create_button = designFunctions.generate_button("Create New Work")
        self.layout.addWidget(self.create_button)
        self.remove_button = designFunctions.generate_button("Remove Works", checkable=True)
        self.layout.addWidget(self.remove_button)
        self.open_button = designFunctions.generate_button("Open Work")
        self.layout.addWidget(self.open_button)

        super().__init__("Works", QSize(900, 700), self.layout)

        self.removable_items = removableItemsHolder.RemovableItemsHolder(self.create_button, self.remove_button,
                                                                         workCreationWidget.WorkCreationWidget,
                                                                         workSummary.WorkSummary, workPage.WorkPage)

        self.layout.addWidget(self.removable_items)

        self.create_button.clicked.connect(self.removable_items.on_create_clicked)
        self.remove_button.clicked.connect(self.removable_items.on_remove_clicked)
        self.open_button.clicked.connect(self.open_work)

    def open_work(self):
        file = str(QFileDialog.getExistingDirectory(parent=self, caption="Select Directory", options=QFileDialog.ShowDirsOnly))
        self.load_state(file)

    # Asks user for closing confirmation, and saves information
    def closeEvent(self, event):
        message = QMessageBox.question(self, "Message", "Are you sure you want to quit?", QMessageBox.Yes, QMessageBox.No)
        if message == QMessageBox.Yes:
            self.save_state()
            event.accept()
        else:
            event.ignore()

    def save_state(self):
        message_box = QMessageBox(icon=QMessageBox.Information, text="Please wait...")
        message_box.show()
        # For each work:
        works = self.removable_items.get_parts()
        for work_name in self.removable_items.get_parts().keys():
            cur_path = QFileDialog.getExistingDirectory(parent=self, caption="Select Directory", options=QFileDialog.ShowDirsOnly)
            # Save title, description, and tags
            work_summary_file = open(os.path.join(cur_path, work_name + "-summary.txt"), "w+")
            summary_string = "_TITLE_" + work_name + "_TITLE_TAGS_" + works[work_name][0].get_tags() \
                  + "_TAGS_DESCRIPTION_" + works[work_name][0].get_description() + "_DESCRIPTION_"
            work_summary_file.write(summary_string)
            work_summary_file.close()
            # For each part:
            work_parts = works[work_name][1].get_parts()
            part_index = 1
            for part_name in work_parts.keys():
                # New directory
                dir_path = os.path.join(cur_path, "part" + str(part_index) + ".dir")
                os.mkdir(dir_path)
                # Save part title and synopsis
                part_header_file = open(os.path.join(dir_path, "header.txt"), "w+")
                part_header_string = "_TITLE_" + part_name + "_TITLE_SYNOPSIS_" + work_parts[part_name][0].get_synopsis() + "_SYNOPSIS_"
                part_header_file.write(part_header_string)
                part_header_file.close()
                # For each box:
                boxes = work_parts[part_name][1].get_all_boxes()
                box_index = 1
                for box in boxes:
                    box_file = open(os.path.join(dir_path, "box" + str(box_index) + ".txt"), "w+")
                    box_str = "_BUTTON_" + box.text() + "_BUTTON_TEXT_" + box.to_html() + "_TEXT_"
                    box_file.write(box_str)
                    box_file.close()
                    box_index += 1
                part_index += 1
        message_box.setText("Finished. Bye!")