import os

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap, QTextDocument
from PyQt5.QtWidgets import QFileDialog, QLabel, QMessageBox, QStyle, QVBoxLayout

import designFunctions
import partSummary
import removableItemsHolder
import scrollableWindow
import workCreationWidget
import workPage
import workSummary
import writingWindow


class WorksWindow(scrollableWindow.ScrollableWindow):
    """ScrollableWindow for displaying all works"""
    def __init__(self):
        self.layout = QVBoxLayout()
        self.img = QPixmap("writing_icon.png")
        self.img_label = QLabel()
        self.create_button = designFunctions.generate_button("Create New Work")
        self.open_button = designFunctions.generate_button("Open Work")
        self.help_button = designFunctions.generate_button("")
        self.add_client_secrets_button = designFunctions.generate_button("Add Client Secrets")
        super().__init__("Works", QSize(1000, 800), self.layout)
        self.removable_items = removableItemsHolder.RemovableItemsHolder(self, self.create_button, None,
                                                                         workCreationWidget.WorkCreationWidget,
                                                                         workSummary.WorkSummary, workPage.WorkPage, None)
        self.init_ui()

    def init_ui(self):
        """Initializes UI for WorksWindow"""
        self.img_label.setPixmap(self.img)
        self.layout.addWidget(self.img_label)
        self.layout.addWidget(self.create_button)
        self.layout.addWidget(self.open_button)
        self.layout.addWidget(self.help_button)
        self.layout.addWidget(self.add_client_secrets_button)
        self.layout.addWidget(self.removable_items)

        pixmapi = getattr(QStyle, "SP_FileDialogInfoView")
        icon = self.style().standardIcon(pixmapi)
        self.help_button.setIcon(icon)

        self.create_button.clicked.connect(self.removable_items.on_create_clicked)
        self.open_button.clicked.connect(self.open_work)
        self.help_button.clicked.connect(self.on_help)
        self.add_client_secrets_button.clicked.connect(self.on_add_secret)

    def parse_holders(self, holders_path):
        """Takes holders_path: string, returns [[placeholder names][corresponding color names]]"""
        text = self.get_text(holders_path)
        info = [[], []]
        if text == "_HOLDERS__HOLDERS_":
            return info
        paired_info = text.split("_HOLDER_")
        for pair in paired_info:
            if pair != "":
                info[0].append(pair.split(";")[0])
                info[1].append(pair.split(";")[1])
        return info

    def parse_summary(self, summary_path):
        """Takes summary_path: string, returns [title: string, tags: QTextDocument, description: QTextDocument]"""
        text = self.get_text(summary_path)
        return [text.split("_TITLE_")[1], QTextDocument(text.split("_TAGS_")[1]), QTextDocument(text.split("_DESCRIPTION_")[1])]

    def parse_part(self, part_summary_path):
        """Takes part_summary_path: string, returns [title: string, synopsis text: QTextDocument]"""
        text = self.get_text(part_summary_path)
        return [text.split("_TITLE_")[1], QTextDocument(text.split("_SYNOPSIS_")[1])]

    def parse_box_info(self, box_info_path):
        """Takes box_info_path: string, returns [button text: string, text: string, comments: string]"""
        text = self.get_text(box_info_path)
        return [text.split("_BUTTON_")[1], text.split("_TEXT_")[1], text.split("_COMMENTS_")[1]]

    def parse_box_order_info(self, box_order_path):
        """Takes box_order_path: string, returns [CollapsableBox button texts]"""
        text = self.get_text(box_order_path)
        return text.split(";")

    def get_text(self, path):
        """Takes path: string, returns text from specified file"""
        file = open(path, "r")
        text = file.read()
        file.close()
        return text

    def load_state(self, dir):
        """Takes dir: string, loads all work files from specified directory"""
        if os.path.exists(os.path.join(dir, "summary.txt")):
            work_info = self.parse_summary(os.path.join(dir, "summary.txt"))
            work_page = workPage.WorkPage(self, work_info[0], work_info[1], work_info[2], dir)
            work_summary = workSummary.WorkSummary(self, self.removable_items, work_info[0], work_info[1], work_info[2], work_page)
            self.removable_items.add_part(work_info[0], work_summary, work_page)
            self.removable_items.add_widget(work_summary)

            # For each part:
            for file_name in os.listdir(dir):
                part_path = os.path.join(dir, file_name)
                if os.path.isdir(part_path):
                    # Header / Summary Info
                    part_info = self.parse_part(os.path.join(part_path, "header.txt"))
                    writing_window = writingWindow.WritingWindow(work_page, part_info[0], part_path)
                    part_summary = partSummary.PartSummary(work_page, work_page.removable_items, part_info[0], part_info[1])
                    work_page.removable_items.add_part(part_info[0], part_summary, writing_window)
                    work_page.removable_items.add_widget(part_summary)
                    # Placeholders set up
                    placeholders_info = self.parse_holders(os.path.join(part_path, "placeholders.txt"))
                    writing_window.add_placeholders(placeholders_info[0], placeholders_info[1])
                    # For each box
                    box_order_info = self.parse_box_order_info(os.path.join(part_path, "box_order.txt"))
                    for box_name in box_order_info:
                        if box_name != "":
                            box_file_path = os.path.join(part_path, "box" + box_name + ".txt")
                            box_info = self.parse_box_info(box_file_path)
                            writing_window.add_box(box_info[0], box_info[1], box_info[2])

    def on_help(self):
        """Handles help request by displaying message with useful information"""
        msg = QMessageBox()
        msg.setWindowTitle("Help")
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
        """Handles open work request, prompts user for directory to load work from"""
        dir = str(QFileDialog.getExistingDirectory(parent=self, caption="Select Directory", options=QFileDialog.ShowDirsOnly))
        if dir != "":
            self.load_state(dir)

    def on_add_secret(self):
        """Adds client secret to current directory for GDrive upload"""
        secrets_file = QFileDialog.getOpenFileName()
        if secrets_file != None and "client_secrets.json" in secrets_file:
            file = open(os.path.join(os.getcwd(), "client_secrets.json"), "w+")
            file.write(secrets_file.read())
            file.close()