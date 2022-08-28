from PyQt5.QtCore import QSize

import designFunctions
import removableItemsHolder
import workCreationWidget
import workSummary
import workPage
import scrollableWindow
from PyQt5.QtWidgets import QVBoxLayout, QFileDialog, QMessageBox


class WorksWindow(scrollableWindow.ScrollableWindow):
    def __init__(self):
        self.layout = QVBoxLayout()
        self.create_button = designFunctions.generate_button("Create New Work")
        self.layout.addWidget(self.create_button)
        self.remove_button = designFunctions.generate_button("Remove Works", checkable=True)
        self.layout.addWidget(self.remove_button)
        self.open_button = designFunctions.generate_button("Open Work")
        self.layout.addWidget(self.open_button)

        super().__init__("Works", QSize(900, 700), self.layout)

        self.removable_items = removableItemsHolder.RemovableItemsHolder(self.create_button, self.remove_button,
                                                                         workCreationWidget.WorkCreationWidget,
                                                                         workSummary.WorkSummary, workPage.WorkPage)

        self.layout.addWidget(self.removable_items)

        self.create_button.clicked.connect(self.removable_items.on_create_clicked)
        self.remove_button.clicked.connect(self.removable_items.on_remove_clicked)
        self.open_button.clicked.connect(self.open_work)

    def open_work(self):
        file = str(QFileDialog.getExistingDirectory(parent=self, caption="Select Directory", options=QFileDialog.ShowDirsOnly))

    def closeEvent(self, event):
        message = QMessageBox.question(self, "Message", "Are you sure you want to quit?", QMessageBox.Yes, QMessageBox.No)
        if message == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()