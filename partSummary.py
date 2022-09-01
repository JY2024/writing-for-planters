from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QCheckBox, QHBoxLayout, QVBoxLayout, QWidget

import designFunctions


class PartSummary(QWidget):
    """QWidget for storing work part information"""
    def __init__(self, parent, item_holder, title, synopsis):
        super().__init__()
        self.parent = parent
        self.item_holder = item_holder
        self.title = title
        self.title_button = designFunctions.generate_button(text=title, border=True, size=QSize(400, 30),
                                                            background_color="rgb(196,235,196)"
        )
        self.check_box = QCheckBox()
        self.synopsis_label = designFunctions.generate_textEdit(doc=synopsis, font_size="14px", border=True,
                                                                size=QSize(600, 200))
        self.top_layout = QHBoxLayout()
        self.main_layout = QVBoxLayout()
        self.init_ui()

    def init_ui(self):
        """Initializes UI for PartSummary"""
        self.setMinimumSize(QSize(650, 250))
        self.setMaximumSize(QSize(650, 250))

        self.top_layout.addWidget(self.title_button)
        self.check_box.hide()
        self.top_layout.addWidget(self.check_box)
        self.main_layout.addLayout(self.top_layout)
        self.main_layout.addWidget(self.synopsis_label)
        self.setLayout(self.main_layout)

        self.title_button.clicked.connect(self.on_title_clicked)

    def on_title_clicked(self):
        """Handles title click event, opens specified part and closes WorkPage"""
        self.item_holder.open_part(self.title)
        self.parent.close()

    def get_synopsis(self):
        """Returns synopsis text"""
        return self.synopsis_label.toPlainText()