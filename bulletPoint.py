from PyQt5.QtWidgets import QWidget, QPushButton, QCheckBox, QHBoxLayout


class BulletPoint(QHBoxLayout):
    def __init__(self, text, my_parent):
        self.my_parent = my_parent
        super().__init__(my_parent)
        self.button = QPushButton(text)
        self.checkBox = QCheckBox()
        self.addWidget(self.button)
        self.addWidget(self.checkBox)
        self.checkBox.hide()

        self.button.clicked.connect(self.on_clicked)

    def on_clicked(self):
        self.my_parent.bulletPoint_was_clicked(self)

    def toggle_checkbox(self):
        if self.checkBox.isVisible():
            self.checkBox.hide()
        else:
            self.checkBox.show()

    def checkBox_selected(self):
        return self.checkBox.isChecked()

    def text(self):
        return self.button.text()

    def removeItems(self):
        self.removeWidget(self.button)
        self.removeWidget(self.checkBox)

    def uncheck(self):
        self.checkBox.setChecked(False)
