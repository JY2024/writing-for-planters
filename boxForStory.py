from PyQt5.QtWidgets import QTextEdit, QSizePolicy

import collapsableBox


class BoxForStory(collapsableBox.CollapsableBox):
    def __init__(self, text, id):
        self.id = id

        self.text_edit = QTextEdit()

        self.text_edit.setMaximumHeight(0)
        self.text_edit.setMinimumHeight(0)
        self.text_edit.setMaximumWidth(940)
        self.text_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        super().__init__(text, self.text_edit)

    def get_id(self):
        return self.id

    def get_written_work(self):
        return self.text_edit.toPlainText()

    def set_writing(self, text):
        self.text_edit.clear()
        self.text_edit.setText(text)

    def set_text_color(self, color):
        if self.text_edit.hasFocus():
            self.text_edit.setTextColor(color)
        else:
            self.comment_text_edit.setTextColor(color)

    def append_text(self, text):
        if self.text_edit.hasFocus():
            self.text_edit.insertPlainText(text)
        else:
            super().append_text(text)

    def has_placeholder(self, action):
        return action in self.get_written_work()

    def toggle_italics(self):
        self.text_edit.setFontItalic(not self.text_edit.fontItalic())