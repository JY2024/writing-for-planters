from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel


class CustomDialog(QDialog):
    def __init__(self, parent, title, size, widget, ok_method, reject_method):
        super().__init__(parent)

        self.setWindowTitle(title)
        self.ok_method = ok_method
        self.reject_method = reject_method
        self.setFixedSize(size)
        self.mainWidget = widget

        buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.on_ok)
        self.buttonBox.rejected.connect(self.on_reject)

        self.layout = QVBoxLayout()
        self.layout.addWidget(widget)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def on_ok(self):
        self.accept()
        if not isinstance(self.mainWidget, QLabel):
            self.ok_method(self.mainWidget)
        else:
            self.ok_method()

    def on_reject(self):
        self.reject()
        if self.reject_method != None:
            self.reject_method()