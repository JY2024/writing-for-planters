from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QVBoxLayout, QWidget

import designFunctions


class WorkSummary(QWidget):
    """QWidget for displaying work information: title, tag, and description"""
    def __init__(self, parent, item_holder, title, tags, description, matching_part):
        super().__init__()
        self.parent = parent
        self.item_holder = item_holder
        self.matching_part = matching_part

        self.title_button = designFunctions.generate_button(title, background_color="rgb(196,235,196)", border=True,
                                                           font_size="20px", size=QSize(600, 50))
        self.tag_label = designFunctions.generate_textEdit(tags, border=True, font_size="14px",
                                                       size=QSize(600, 100))
        self.description_label = designFunctions.generate_textEdit(description, border=True, font_size="14px",
                                                                   size=QSize(600, 200))
        self.main_layout = QVBoxLayout()
        self.init_ui()

    def init_ui(self):
        """Initializes UI for WorkSummary"""
        self.setMinimumSize(QSize(620, 400))
        self.setMaximumSize(QSize(620, 400))

        self.main_layout.addWidget(self.title_button)
        self.main_layout.addWidget(self.tag_label)
        self.main_layout.addWidget(self.description_label)
        self.setLayout(self.main_layout)

        self.title_button.clicked.connect(self.on_title_clicked)
        self.tag_label.textChanged.connect(self.on_text_changed)
        self.description_label.textChanged.connect(self.on_text_changed)

    def on_title_clicked(self):
        """Handles title button being clicked, opens matching WorkPage and closes this window"""
        self.item_holder.open_part(self.title_button.text())
        self.parent.close()

    def on_text_changed(self):
        """Handles text change event, sets the tags and description in matching WorkPage to be the same"""
        self.matching_part.set_tags(self.tag_label.toPlainText())
        self.matching_part.set_description(self.description_label.toPlainText())

    def get_title(self):
        """Returns title button text as string"""
        return self.title_button.text()

    def get_tags(self):
        """Returns tag label text"""
        return self.tag_label.toPlainText()

    def get_description(self):
        """Returns description label text"""
        return self.description_label.toPlainText()


