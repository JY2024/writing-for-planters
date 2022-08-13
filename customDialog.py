from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel


class CustomDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)

        self.setWindowTitle("Deletion")

        buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.on_ok)
        self.buttonBox.rejected.connect(self.on_reject)

        self.layout = QVBoxLayout()
        message = QLabel("Are you sure you want to delete these sections?\nTHIS IS NOT REVERSIBLE.")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def on_ok(self):
        self.accept()
        self.parent().on_ok()

    def on_reject(self):
        self.reject()
        self.parent().on_reject()