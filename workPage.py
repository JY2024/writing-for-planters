import os

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QKeySequence, QTextDocument
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtWidgets import QHBoxLayout, QMessageBox, QPushButton, QShortcut, QStyle, QTextEdit, QVBoxLayout

import designFunctions
import partCreationWidget
import partSummary
import removableItemsHolder
import scrollableWindow
import writingWindow


class Popup(scrollableWindow.ScrollableWindow):
    """Scrollable popup to display a document"""
    def __init__(self, doc):
        self.layout = QVBoxLayout()
        self.text_edit = QTextEdit()
        self.text_edit.setDocument(doc)
        self.text_edit.setReadOnly(True)
        self.layout.addWidget(self.text_edit)

        super().__init__("Preview", QSize(1000, 700), self.layout)
        self.setStyleSheet("background-color: white")


class WorkPage(scrollableWindow.ScrollableWindow):
    """Scrollable window to view all parts of a work and general work info"""
    def __init__(self, parent, title, tags, description, path):
        self.parent = parent
        self.title = title
        self.path = path
        self.gauth = GoogleAuth()
        self.authorized = False
        self.drive = None
        self.popups = []
        self.mode_msg = QMessageBox()

        self.back_button = designFunctions.generate_button(background_color="light grey", size=QSize(30,30))
        self.preview_button = designFunctions.generate_button("Preview")
        self.export_button = designFunctions.generate_button("Export")
        self.local_save_button = designFunctions.generate_button("Local Save")
        self.title_label = designFunctions.generate_label(title, font_size="30px", bold=True)
        self.tag_label = designFunctions.generate_textEdit(tags, font_size="14px", border=True, size=QSize(700, 100),
                                                           read_only=True, alignment=Qt.AlignCenter)
        self.description_label = designFunctions.generate_textEdit(description, font_size="14px", border=True,
                                                               size=QSize(700, 150), read_only=True,
                                                                   alignment=Qt.AlignCenter)
        self.add_part_button = designFunctions.generate_button("Add Part")
        self.remove_button = designFunctions.generate_button("Remove Part", checkable=True)
        self.removable_items = removableItemsHolder.RemovableItemsHolder(self, self.add_part_button, self.remove_button,
                                                                         partCreationWidget.PartCreationWidget,
                                                                         partSummary.PartSummary,
                                                                         writingWindow.WritingWindow, path)

        self.main_layout = QVBoxLayout()
        self.top_layout = QHBoxLayout()
        super().__init__(title, QSize(1000, 800), self.main_layout)
        self.init_ui()

    def init_ui(self):
        """Initializes UI for WorkPage"""
        self.main_layout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.main_layout.addWidget(self.back_button)
        self.top_layout.addWidget(self.preview_button)
        self.top_layout.addWidget(self.export_button)
        self.top_layout.addWidget(self.local_save_button)
        self.main_layout.addLayout(self.top_layout)
        self.main_layout.addWidget(self.title_label)
        self.main_layout.addWidget(self.tag_label)
        self.main_layout.addWidget(self.description_label)
        self.main_layout.addWidget(self.add_part_button)
        self.main_layout.addWidget(self.remove_button)
        self.main_layout.addWidget(self.removable_items)

        pixmapi = getattr(QStyle, "SP_ArrowBack")
        icon = self.style().standardIcon(pixmapi)
        self.back_button.setIcon(icon)

        self.mode_msg.setWindowTitle("Export")
        self.mode_msg.addButton(QPushButton("Download/Print"), QMessageBox.YesRole)
        self.mode_msg.addButton(QPushButton("Upload to GDrive"), QMessageBox.YesRole)
        self.mode_msg.addButton(QPushButton("Cancel"), QMessageBox.RejectRole)

        self.back_button.clicked.connect(self.on_back)
        self.preview_button.clicked.connect(self.on_preview)
        self.export_button.clicked.connect(self.on_export)
        self.local_save_button.clicked.connect(self.on_local_save)
        self.add_part_button.clicked.connect(self.removable_items.on_create_clicked)
        self.remove_button.clicked.connect(self.removable_items.on_remove_clicked)
        self.mode_msg.buttonClicked.connect(self.on_mode_clicked)

        save_shortcut = QShortcut(QKeySequence(self.tr("Ctrl+S")), self)
        save_shortcut.activated.connect(self.on_local_save)

    def on_mode_clicked(self, btn):
        """Takes btn: QPushButton, executes the approrpiate response to user request (print or upload)"""
        if btn.text() == "Download/Print":
            self.on_print()
        elif btn.text() == "Upload to GDrive":
            self.on_upload()

    def on_back(self):
        """Closes this WorkPage and opens WorksWindow"""
        self.parent.show()
        self.close()

    def on_export(self):
        """Displays export message and options"""
        self.mode_msg.show()

    def on_preview(self):
        """Displays all text in work in a preview window"""
        self.popups.clear()
        popup = Popup(self.get_doc())
        popup.show()
        self.popups.append(popup)

    def on_print(self):
        """Handles user request to print"""
        printer = QPrinter(mode=QPrinter.HighResolution)
        dlg = QPrintDialog(printer, self)
        if dlg.exec() == QPrintDialog.Accepted:
            self.get_doc().print(dlg.printer())

    def on_local_save(self):
        """Saves the work's title, tags, and description in work's directory, as well as all parts and synopses"""
        # Save title, description, and tags
        work_summary_file = open(os.path.join(self.path, "summary.txt"), "w+")
        summary_string = "_TITLE_" + self.title + "_TITLE_TAGS_" + self.tag_label.toPlainText() \
                         + "_TAGS_DESCRIPTION_" + self.description_label.toPlainText() + "_DESCRIPTION_"
        work_summary_file.write(summary_string)
        work_summary_file.close()

        # Save the part synopsis and titles
        parts = self.removable_items.get_parts()
        for part_name in parts.keys():
            part_path = parts[part_name][1].get_path()
            part_header_file = open(os.path.join(part_path, "header.txt"), "w+")
            part_header_string = "_TITLE_" + part_name + "_TITLE_SYNOPSIS_" + parts[part_name][0].get_synopsis() + "_SYNOPSIS_"
            part_header_file.write(part_header_string)
            part_header_file.close()

    def on_upload(self):
        """Locally saves, authorizes user to GDrive and uploads all text to a file in GDrive"""
        self.on_local_save()
        parts = self.removable_items.get_parts()
        for key in parts.keys():
            parts[key][1].on_local_save()

        if not self.authorized:
            self.gauth.LocalWebserverAuth()
            if self.gauth == "":
                return
            self.authorized = True
            self.drive = GoogleDrive(self.gauth)

        file = self.drive.CreateFile({'title': self.title_label.text() + '.txt'})
        file.SetContentString(self.get_all_text(self.removable_items.get_parts()))
        file.Upload()

    def get_doc(self):
        """Returns all work's text as QTextDocument"""
        text = self.get_all_text(self.removable_items.get_parts())
        doc = QTextDocument()
        doc.setPlainText(text)
        return doc

    def get_all_text(self, parts):
        """Takes parts: Dict and returns all the text in these parts as string"""
        text = ""
        for key in parts.keys():
            text += "\n" + parts[key][1].get_all_text()
        return text

    def get_parts(self):
        """Returns all parts: Dict"""
        return self.removable_items.get_parts()

    def set_tags(self, text):
        """Takes text: string, sets tags to QTextDocument containing text"""
        self.tag_label.setDocument(QTextDocument(text))

    def set_description(self, text):
        """Takes text: string, sets description to QTextDocument containing text"""
        self.description_label.setDocument(QTextDocument(text))
