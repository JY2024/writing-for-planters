from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QMainWindow, QWidget, QScrollArea, QLabel, QVBoxLayout, QPushButton

import customDialog
import partCreationWidget
import writingWindow
import partSummary


class WorkPage(QMainWindow):
    def __init__(self, title, tags, description):
        super().__init__()
        
        self.totalChapters = 0
        self.parts = {}

        self.setWindowTitle(title)
        self.resize(QSize(900, 700))
        self.setMaximumSize(QSize(900, 700))
        self.titleLabel = QLabel(title)
        self.titleLabel.setStyleSheet("font: bold 40px")
        self.titleLabel.setAlignment(Qt.AlignCenter)

        self.tagLabel = QLabel(tags)
        self.tagLabel.setStyleSheet("background-color:white;border:1px solid black;font:14px")
        self.tagLabel.setMinimumSize(QSize(800, 200))
        self.tagLabel.setMaximumSize(QSize(800, 300))
        self.tagLabel.setAlignment(Qt.AlignCenter)
        self.descriptionLabel = QLabel(description)
        self.descriptionLabel.setStyleSheet("background-color:white;border:1px solid black;font:14px")
        self.descriptionLabel.setMinimumSize(QSize(800, 200))
        self.descriptionLabel.setMaximumSize(QSize(800, 300))
        self.descriptionLabel.setAlignment(Qt.AlignCenter)
        self.addPartButton = QPushButton("Add Part")

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.titleLabel)
        self.mainLayout.addWidget(self.tagLabel)
        self.mainLayout.addWidget(self.descriptionLabel)
        self.mainLayout.addWidget(self.addPartButton)

        # Finish set up
        widget = QWidget()
        widget.setLayout(self.mainLayout)
        self.scroll = QScrollArea()
        self.scroll.setWidget(widget)
        self.scroll.setWidgetResizable(True)
        self.setCentralWidget(self.scroll)
        
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

