from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QMainWindow, QWidget, QScrollArea, QLabel, QVBoxLayout, QPushButton

import customDialog
import partCreationWidget
import writingWindow
import partSummary
import designFunctions
import scrollableWindow


class WorkPage(scrollableWindow.ScrollableWindow):
    def __init__(self, title, tags, description):
        self.totalChapters = 0
        self.parts = {}

        self.titleLabel = designFunctions.generate_label(title, font_size="40px", bold=True, alignment=Qt.AlignCenter)

        self.tagLabel = designFunctions.generate_label(tags, font_size="14px", border=True, size=QSize(800, 200),
                                                       background_color="white")
        self.descriptionLabel = designFunctions.generate_label(description, font_size="14px", border=True,
                                                               size=QSize(800, 200), background_color="white")
        self.addPartButton = QPushButton("Add Part")

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.titleLabel)
        self.mainLayout.addWidget(self.tagLabel)
        self.mainLayout.addWidget(self.descriptionLabel)
        self.mainLayout.addWidget(self.addPartButton)

        super().__init__(title, QSize(900, 700), self.mainLayout)
        
        self.addPartButton.clicked.connect(self.on_add_clicked)
        
    def on_add_clicked(self):
        partCreation = partCreationWidget.PartCreationWidget()
        dlg = customDialog.CustomDialog(
            self, "Create Part", QSize(500, 500), partCreation, self.on_add_ok, self.toggle_all_checkboxes
        )
        dlg.exec()
    
    def on_add_ok(self, widget):
        myPartSummary = partSummary.PartSummary(self, widget.get_title(), widget.get_description(), self.totalChapters + 1)
        self.mainLayout.addWidget(myPartSummary)
        partWritingWindow = writingWindow.WritingWindow(widget.get_title())
        self.parts[widget.get_title()] = [myPartSummary, partWritingWindow]
        self.totalChapters += 1
    
    def toggle_all_checkboxes(self):
        for key, value in self.parts.items():
            value[0].toggle_checkbox_visible()

    def open_part(self, title):
        self.parts[title][1].show()

