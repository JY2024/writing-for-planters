from PyQt5.QtWidgets import QWidget, QPushButton, QCheckBox, QHBoxLayout


class BulletPoint(QHBoxLayout):
    def __init__(self, text):
        super().__init__()
        self.button = QPushButton(text)
        self.checkBox = QCheckBox()
        self.addWidget(self.button)
        self.addWidget(self.checkBox)

        self.checkBox.hide()

    def toggle_checkbox(self):
        if self.checkBox.isVisible():
            self.checkBox.hide()
        else:
            self.checkBox.show()

    def checkBox_selected(self):
        return self.checkBox.isChecked()

