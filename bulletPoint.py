from PyQt5.QtWidgets import QCheckBox, QHBoxLayout, QPushButton


class BulletPoint(QHBoxLayout):
    """QHBoxLayout for holding a bulletpoint button and checkbox"""
    def __init__(self, text, my_parent, my_box, id):
        self.my_parent = my_parent
        self.my_box = my_box
        self.id = id

        super().__init__(my_parent)

        self.button = QPushButton(text)
        self.check_box = QCheckBox()
        self.init_ui()

    def init_ui(self):
        """Initializes UI for BulletPoint"""
        self.button.setStyleSheet("background-color: light grey")
        self.addWidget(self.button)
        self.addWidget(self.check_box)
        self.check_box.hide()
        self.button.clicked.connect(self.on_clicked)

    def remove_items(self):
        """Removes all items from BulletPoint layout"""
        self.removeWidget(self.button)
        self.removeWidget(self.check_box)

    def on_clicked(self):
        """Notifies WritingWindow that this BulletPoint was clicked"""
        self.my_parent.bulletPoint_was_clicked(self)

    def get_text(self):
        """Returns button text"""
        return self.button.text()

    def get_id(self):
        """Returns id"""
        return self.id

    def uncheck(self):
        """Returns whether the checkbox is checked"""
        self.check_box.setChecked(False)

    def set_button_text(self, text):
        """Takes text: string, sets this button's text to text"""
        self.button.setText(text)

    def set_box_text(self, text):
        """Takes text, sets BulletPoint's matching box's button to text"""
        self.my_box.set_button_text(text)