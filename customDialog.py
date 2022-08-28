from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel

class CustomDialog(QDialog):
    def __init__(self, parent, title, size, widget, ok_method, reject_method):
        super().__init__(parent)

        self.setWindowTitle(title)
        self.ok_method = ok_method
        self.reject_method = reject_method
        self.setFixedSize(size)
        self.main_widget = widget

        buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.button_box = QDialogButtonBox(buttons)
        self.button_box.accepted.connect(self.on_ok)
        self.button_box.rejected.connect(self.on_reject)

        self.layout = QVBoxLayout()
        self.layout.addWidget(widget)
        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)

    def on_ok(self):
        self.accept()
        if self.ok_method != None:
            if not isinstance(self.main_widget, QLabel):
                self.ok_method(self.main_widget)
            else:
                self.ok_method()

    def on_reject(self):
        self.reject()
        if self.reject_method != None:
            self.reject_method()