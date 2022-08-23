from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QLabel

import customDialog
import workCreationWidget
import workSummary


class RemovableItemsHolder(QGroupBox):
    def __init__(self, remove_button, part_creation_widget, part_summary, part):
        super().__init__()
        self.part_creation_widget = part_creation_widget
        self.part_summary = part_summary
        self.part = part
        self.remove_button = remove_button
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.parts = {}

    def on_create_clicked(self):
        helper_widget = self.part_creation_widget()
        dlg = customDialog.CustomDialog(
            self, "Create", QSize(500, 500), helper_widget, self.on_create_ok, self.toggle_all_checkboxes
        )
        dlg.exec()

    def on_create_ok(self, widget):
        my_part_summary = None
        my_part = None
        if isinstance(widget, workCreationWidget.WorkCreationWidget):
            my_part_summary = self.part_summary(self, widget.get_title(), widget.get_tags(), widget.get_description())
            my_part = self.part(widget.get_title(), widget.get_tags(), widget.get_description())
        else:
            my_part_summary = self.part_summary(self, widget.get_title(), widget.get_description(), len(self.parts) + 1)
            my_part = self.part(widget.get_title())
        self.main_layout.addWidget(my_part_summary)
        self.parts[widget.get_title()] = [my_part_summary, my_part]

    def toggle_all_checkboxes(self):
        for key, value in self.parts.items():
            value[0].toggle_checkbox_visible()

    def open_part(self, title):
        self.parts[title][1].show()

    def on_remove_clicked(self):
        if self.remove_button.isChecked():
            self.toggle_all_checkboxes()
        else:
            dlg = customDialog.CustomDialog(
                self, "Remove", QSize(300, 100),
                QLabel("Are you sure you want to remove these?\nTHIS IS NOT REVERSIBLE."), self.on_remove_ok,
                self.toggle_all_checkboxes
            )
            dlg.exec()

    def on_remove_ok(self):
        for title in list(self.parts):
            summary = self.works[title][0]
            if summary.is_checked():
                self.main_layout.removeWidget(summary)
                self.parts.pop(title)
        self.toggle_all_checkboxes()

    def on_enter_edit_ok(self):
        pass

    def on_edit_ok(self):
        pass

    def on_edit_reject(self):
        pass


