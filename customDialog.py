from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel


class CustomDialog(QDialog):
    def __init__(self, parent, title, text, ok_method, reject_method):
        super().__init__(parent)

        self.setWindowTitle(title)
        self.ok_method = ok_method
        self.reject_method = reject_method

        buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.on_ok)
        self.buttonBox.rejected.connect(self.on_reject)

        self.layout = QVBoxLayout()
        message = QLabel(text)
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def on_ok(self):
        self.accept()
        self.ok_method()

    def on_reject(self):
        self.reject()
        self.reject_method()