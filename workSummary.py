from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QCheckBox

import designFunctions


class WorkSummary(QWidget):
    def __init__(self, parent, title, tags, description):
        super().__init__()
        self.my_parent = parent

        self.setMinimumSize(QSize(500, 500))
        self.setMaximumSize(QSize(500, 500))

        self.top_layout = QHBoxLayout()

        self.title_button = designFunctions.generate_button(title, background_color="yellow", border=True, bold=True,
                                                           font_size="20px", size=QSize(200, 50))
        self.top_layout.addWidget(self.title_button)
        self.check_box = QCheckBox()
        self.check_box.hide()
        self.top_layout.addWidget(self.check_box)
        self.tag_label = designFunctions.generate_label(tags, border=True, font_size="14px", background_color="white",
                                                       size=QSize(400, 200))
        self.description_label = designFunctions.generate_label(description, border=True, font_size="14px",
                                                               background_color="white", size=QSize(400, 200))

        self.main_layout = QVBoxLayout()

        self.main_layout.addLayout(self.top_layout)
        self.main_layout.addWidget(self.tag_label)
        self.main_layout.addWidget(self.description_label)
        self.setLayout(self.main_layout)

        self.title_button.clicked.connect(self.on_title_clicked)

    def on_title_clicked(self):
        self.my_parent.open_part(self.title_button.text())

    def toggle_checkbox_visible(self):
        if self.check_box.isVisible():
            self.check_box.hide()
        else:
            self.check_box.show()

    def is_checked(self):
        return self.check_box.isChecked()

    def get_title(self):
        return self.title_button.text()

