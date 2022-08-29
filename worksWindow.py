import os
import pathlib

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QTextDocument

import designFunctions
import partSummary
import removableItemsHolder
import workCreationWidget
import workSummary
import workPage
import scrollableWindow
from PyQt5.QtWidgets import QVBoxLayout, QFileDialog, QMessageBox

import writingWindow


class WorksWindow(scrollableWindow.ScrollableWindow):
    def __init__(self):
        self.layout = QVBoxLayout()
        self.create_button = designFunctions.generate_button("Create New Work")
        self.layout.addWidget(self.create_button)
        self.open_button = designFunctions.generate_button("Open Work")
        self.layout.addWidget(self.open_button)

        super().__init__("Works", QSize(900, 700), self.layout)

        self.removable_items = removableItemsHolder.RemovableItemsHolder(self.create_button, None,
                                                                         workCreationWidget.WorkCreationWidget,
                                                                         workSummary.WorkSummary, workPage.WorkPage, None)

        self.layout.addWidget(self.removable_items)

        self.create_button.clicked.connect(self.removable_items.on_create_clicked)
        self.open_button.clicked.connect(self.open_work)

    def open_work(self):
        dir = str(QFileDialog.getExistingDirectory(parent=self, caption="Select Directory", options=QFileDialog.ShowDirsOnly))
        if dir != "":
            self.load_state(dir)

    def load_state(self, dir):
        if os.path.exists(os.path.join(dir, "summary.txt")):
            work_info = self.parse_summary(os.path.join(dir, "summary.txt"))
            work_page = workPage.WorkPage(work_info[0], work_info[1], work_info[2], dir)
            work_summary = workSummary.WorkSummary(self.removable_items, work_info[0], work_info[1], work_info[2], work_page)
            self.removable_items.add_part(work_info[0], work_summary, work_page)
            self.removable_items.add_widget(work_summary)

            # For each part:
            for file_name in os.listdir(dir):
                part_path = os.path.join(dir, file_name)
                if os.path.isdir(part_path):
                    part_info = self.parse_part(os.path.join(part_path, "header.txt"))
                    writing_window = writingWindow.WritingWindow(part_info[0], part_path)
                    part_summary = partSummary.PartSummary(work_page.removable_items, part_info[0], part_info[1])
                    work_page.removable_items.add_part(part_info[0], part_summary, writing_window)
                    work_page.removable_items.add_widget(part_summary)

                    # For each box
                    for box_file_name in os.listdir(part_path):
                        box_file_path = os.path.join(part_path, box_file_name)
                        if os.path.isfile(box_file_path) and "header" not in box_file_path:
                            box_info = self.parse_box_info(box_file_path)
                            writing_window.add_box(box_info[0], box_info[1], box_info[2])

    def parse_summary(self, summary_path):
        file = open(summary_path, "r")
        text = file.read()
        return [text.split("_TITLE_")[1], QTextDocument(text.split("_TAGS_")[1]), QTextDocument(text.split("_DESCRIPTION_")[1])]

    def parse_part(self, part_summary_path):
        file = open(part_summary_path, "r")
        text = file.read()
        return [text.split("_TITLE_")[1], QTextDocument(text.split("_SYNOPSIS_")[1])]

    def parse_box_info(self, box_info_path):
        file = open(box_info_path, "r")
        text = file.read()
        return [text.split("_BUTTON_")[1], text.split("_TEXT_")[1], text.split("_COMMENTS_")[1]]