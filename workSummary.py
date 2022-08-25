from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QCheckBox

import designFunctions


class WorkSummary(QWidget):
    def __init__(self, parent, title, tags, description, matching_part):
        super().__init__()
        self.my_parent = parent
        self.matching_part = matching_part

        self.setMinimumSize(QSize(500, 500))
        self.setMaximumSize(QSize(500, 500))

        self.top_layout = QHBoxLayout()

        self.title_button = designFunctions.generate_button(title, background_color="yellow", border=True, bold=True,
                                                           font_size="20px", size=QSize(200, 50))
        self.top_layout.addWidget(self.title_button)
        self.check_box = QCheckBox()
        self.check_box.hide()
        self.top_layout.addWidget(self.check_box)
        self.tag_label = designFunctions.generate_textEdit(tags, border=True, font_size="14px", background_color="white",
                                                       size=QSize(400, 200))
        self.description_label = designFunctions.generate_textEdit(description, border=True, font_size="14px",
                                                               background_color="white", size=QSize(400, 200))

        self.main_layout = QVBoxLayout()

        self.main_layout.addLayout(self.top_layout)
        self.main_layout.addWidget(self.tag_label)
        self.main_layout.addWidget(self.description_label)
        self.setLayout(self.main_layout)

        self.title_button.clicked.connect(self.on_title_clicked)
        self.tag_label.textChanged.connect(self.on_text_changed)
        self.description_label.textChanged.connect(self.on_text_changed)

    def on_title_clicked(self):
        self.my_parent.open_part(self.title_button.text())

    def get_title(self):
        return self.title_button.text()

    def on_text_changed(self):
        self.matching_part.set_tags(self.tag_label.toPlainText())
        self.matching_part.set_description(self.description_label.toPlainText())
