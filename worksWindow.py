from PyQt5.QtCore import QSize

import customDialog
import workCreationWidget
import workSummary
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QScrollArea, QWidget, QPushButton

import writingWindow


class WorksWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Works")
        self.works = {}

        self.resize(QSize(900, 700))
        self.setMaximumSize(QSize(900, 700))
        self.layout = QVBoxLayout()
        self.createButton = QPushButton("Create New Work")
        self.layout.addWidget(self.createButton)

        # Finish set up
        widget = QWidget()
        widget.setLayout(self.layout)
        self.scroll = QScrollArea()
        self.scroll.setWidget(widget)
        self.scroll.setWidgetResizable(True)
        self.setCentralWidget(self.scroll)

        self.createButton.clicked.connect(self.on_create_clicked)

    def on_create_clicked(self):
        workCreation = workCreationWidget.WorkCreationWidget()
        dlg = customDialog.CustomDialog(
            self, "Create New Work", QSize(500, 500), workCreation, self.on_create_ok, None
        )
        dlg.exec()

    def on_create_ok(self, widget):
        work = workSummary.WorkSummary(self, widget.get_title(), widget.get_tags(), widget.get_description())
        self.layout.addWidget(work)
        workWriting = writingWindow.WritingWindow(widget.get_title())
        self.works[widget.get_title()] = workWriting

    def open_work(self, title):
        work = self.works[title].show()