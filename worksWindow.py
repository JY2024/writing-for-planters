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
from PyQt5.QtWidgets import QVBoxLayout, QFileDialog, QMessageBox, QStyle

import writingWindow


class WorksWindow(scrollableWindow.ScrollableWindow):
    def __init__(self):
        self.layout = QVBoxLayout()
        self.create_button = designFunctions.generate_button("Create New Work")
        self.layout.addWidget(self.create_button)
        self.open_button = designFunctions.generate_button("Open Work")
        self.layout.addWidget(self.open_button)
        self.help_button = designFunctions.generate_button("")
        self.layout.addWidget(self.help_button)

        super().__init__("Works", QSize(900, 700), self.layout)

        pixmapi = getattr(QStyle, "SP_FileDialogInfoView")
        icon = self.style().standardIcon(pixmapi)
        self.help_button.setIcon(icon)

        self.removable_items = removableItemsHolder.RemovableItemsHolder(self.create_button, None,
                                                                         workCreationWidget.WorkCreationWidget,
                                                                         workSummary.WorkSummary, workPage.WorkPage, None)

        self.layout.addWidget(self.removable_items)

        self.create_button.clicked.connect(self.removable_items.on_create_clicked)
        self.open_button.clicked.connect(self.open_work)
        self.help_button.clicked.connect(self.on_help)

    def on_help(self):
        msg = QMessageBox()
        msg.setText("[Works Window]\n - Create works and select a directory for the work when prompted." +
                    "\n - OR Select a work directory to open.\n - Edit work tags and descriptions.\n\n" +
                    "[Work Page]\n - Add and remove parts.\n - Edit part summaries.\n - EXPORT to GDrive or print/pdf\n" +
                    " - LOCAL SAVE (Ctrl+S) work to existing work directory\n - PREVIEW as pdf.\n\n[Part Window]\n" +
                    " - LOCAL SAVE (Ctrl+S) work to existing work directory\n - EDIT MODE to rearrange and rename bulletpoints.\n" +
                    " - Tip: Alt+E to enter new bulletpoint.\n - Tip: Ctrl+o to go to top of page\n" +
                    " - Tip: Ctrl+H to add/select new placeholder to insert.\n\t(MANAGE PLACEHOLDERS to see all occurences of one placeholder.")
        msg.setIcon(QMessageBox.Information)
        msg.exec()

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

                    # Placeholders set up
                    placeholders_info = self.parse_holders(os.path.join(part_path, "placeholders.txt"))
                    writing_window.add_placeholders(placeholders_info[0], placeholders_info[1])

                    # For each box
                    for box_file_name in os.listdir(part_path):
                        box_file_path = os.path.join(part_path, box_file_name)
                        if os.path.isfile(box_file_path) and "header" not in box_file_path and "placeholders" not in box_file_path:
                            box_info = self.parse_box_info(box_file_path)
                            writing_window.add_box(box_info[0], box_info[1], box_info[2])

    def parse_holders(self, holders_path):
        text = self.get_text(holders_path)
        info = [[], []]
        paired_info = text.split("_HOLDER_")
        for pair in paired_info:
            if pair != "":
                info[0].append(pair.split(";")[0])
                info[1].append(pair.split(";")[1])
        return info

    def parse_summary(self, summary_path):
        text = self.get_text(summary_path)
        return [text.split("_TITLE_")[1], QTextDocument(text.split("_TAGS_")[1]), QTextDocument(text.split("_DESCRIPTION_")[1])]

    def parse_part(self, part_summary_path):
        text = self.get_text(part_summary_path)
        return [text.split("_TITLE_")[1], QTextDocument(text.split("_SYNOPSIS_")[1])]

    def parse_box_info(self, box_info_path):
        text = self.get_text(box_info_path)
        return [text.split("_BUTTON_")[1], text.split("_TEXT_")[1], text.split("_COMMENTS_")[1]]

    def get_text(self, path):
        file = open(path, "r")
        text = file.read()
        file.close()
        return text