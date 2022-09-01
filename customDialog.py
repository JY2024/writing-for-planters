from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QLabel, QVBoxLayout


class CustomDialog(QDialog):
    """QDialog for displaying a helper widget for creation of another widget"""
    def __init__(self, parent, title, size, widget, ok_method, reject_method):
        super().__init__(parent)
        self.main_widget = widget
        self.ok_method = ok_method
        self.reject_method = reject_method
        self.setWindowTitle(title)
        self.setFixedSize(size)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.init_ui()

    def init_ui(self):
        """Initializes UI for CustomDialog"""
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.main_widget)
        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)
        self.button_box.accepted.connect(self.on_ok)
        self.button_box.rejected.connect(self.on_reject)

    def on_ok(self):
        """Accepts on user choice and calls appropriate accept method"""
        self.accept()
        if self.ok_method != None:
            if not isinstance(self.main_widget, QLabel):
                self.ok_method(self.main_widget)
            else:
                self.ok_method()

    def on_reject(self):
        """Rejects on user choice and calls appropriate reject method"""
        self.reject()
        if self.reject_method != None:
            self.reject_method()