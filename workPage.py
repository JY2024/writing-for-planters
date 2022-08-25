from PyQt5.QtCore import Qt, QSize
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QHBoxLayout

import partCreationWidget
import removableItemsHolder
import writingWindow
import partSummary
import designFunctions
import scrollableWindow


class WorkPage(scrollableWindow.ScrollableWindow):
    def __init__(self, title, tags, description):
        self.export_button = designFunctions.generate_button("Export")
        self.preview_button = designFunctions.generate_button("Preview")
        self.title_label = designFunctions.generate_label(title, font_size="40px", bold=True, alignment=Qt.AlignCenter)

        self.tag_label = designFunctions.generate_label(tags, font_size="14px", border=True, size=QSize(800, 200),
                                                       background_color="white")
        self.description_label = designFunctions.generate_label(description, font_size="14px", border=True,
                                                               size=QSize(800, 200), background_color="white")
        self.add_part_button = QPushButton("Add Part")
        self.remove_button = designFunctions.generate_button("Remove Part", checkable=True)

        self.removable_items = removableItemsHolder.RemovableItemsHolder(self.remove_button,
                                                                         partCreationWidget.PartCreationWidget,
                                                                         partSummary.PartSummary,
                                                                         writingWindow.WritingWindow)

        self.main_layout = QVBoxLayout()
        self.top_layout = QHBoxLayout()
        self.top_layout.addWidget(self.preview_button)
        self.top_layout.addWidget(self.export_button)
        self.main_layout.addLayout(self.top_layout)
        self.main_layout.addWidget(self.title_label)
        self.main_layout.addWidget(self.tag_label)
        self.main_layout.addWidget(self.description_label)
        self.main_layout.addWidget(self.add_part_button)
        self.main_layout.addWidget(self.remove_button)
        self.main_layout.addWidget(self.removable_items)

        super().__init__(title, QSize(900, 700), self.main_layout)
        
        self.add_part_button.clicked.connect(self.removable_items.on_create_clicked)
        self.remove_button.clicked.connect(self.removable_items.on_remove_clicked)
        self.export_button.clicked.connect(self.on_export)
        self.preview_button.clicked.connect(self.on_preview)

    def set_tags(self, text):
        self.tag_label.setText(text)

    def set_description(self, text):
        self.description_label.setText(text)

    def on_export(self):
        printer = QPrinter(mode=QPrinter.HighResolution)
        dlg = QPrintDialog(printer, self)
        if dlg.exec() == QPrintDialog.Accepted:
            self.handle_print()

    def handle_print(self):
        parts = self.removable_items.get_parts()

    def on_preview(self):
        pass

