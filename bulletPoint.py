from PyQt5.QtWidgets import QPushButton, QCheckBox, QHBoxLayout

class BulletPoint(QHBoxLayout):
    def __init__(self, text, my_parent, my_box, id):
        self.id = id
        self.my_parent = my_parent
        self.my_box = my_box
        super().__init__(my_parent)
        self.button = QPushButton(text)
        self.check_box = QCheckBox()
        self.addWidget(self.button)
        self.addWidget(self.check_box)
        self.check_box.hide()

        self.button.clicked.connect(self.on_clicked)

    def on_clicked(self):
        self.my_parent.bulletPoint_was_clicked(self)

    def remove_items(self):
        self.removeWidget(self.button)
        self.removeWidget(self.check_box)

    def uncheck(self):
        self.check_box.setChecked(False)

    def get_text(self):
        return self.button.text()

    def set_text(self, text):
        self.button.setText(text)

    def set_box_text(self, text):
        self.my_box.set_text(text)

    def matching_box(self):
        return self.my_box

    def get_id(self):
        return self.id
