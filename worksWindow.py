from PyQt5.QtCore import QSize

import customDialog
import workCreationWidget
import workSummary
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QScrollArea, QWidget, QPushButton

class WorksWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(QSize(1000, 700))
        self.setMaximumSize(QSize(1000, 700))
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
        work = workSummary.WorkSummary(widget.get_title(), widget.get_tags(), widget.get_description())
        self.layout.addWidget(work)