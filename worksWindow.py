from PyQt5.QtCore import QSize

import customDialog
import workCreationWidget
import workSummary
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QScrollArea, QWidget, QPushButton, QLabel

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
        self.removeButton = QPushButton("Remove Works")
        self.removeButton.setCheckable(True)
        self.removeButton.setChecked(False)
        self.layout.addWidget(self.removeButton)

        # Finish set up
        widget = QWidget()
        widget.setLayout(self.layout)
        self.scroll = QScrollArea()
        self.scroll.setWidget(widget)
        self.scroll.setWidgetResizable(True)
        self.setCentralWidget(self.scroll)

        self.createButton.clicked.connect(self.on_create_clicked)
        self.removeButton.clicked.connect(self.on_remove_clicked)

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
        self.works[widget.get_title()] = [work, workWriting]

    def open_work(self, title):
        self.works[title][1].show()

    def on_remove_clicked(self):
        if self.removeButton.isChecked():
            for key, value in self.works.items():
                value[0].show_checkbox()
        else:
            dlg = customDialog.CustomDialog(
                self, "Remove Works", QSize(300, 100), QLabel("Are you sure you want to remove these works?\nTHIS IS NOT REVERSIBLE."), self.on_remove_ok, self.revert_remove
            )
            dlg.exec()

    def on_remove_ok(self):
        for title in list(self.works):
            summary = self.works[title][0]
            if summary.is_checked():
                self.layout.removeWidget(summary)
                self.works.pop(title)

    def revert_remove(self):
        pass
