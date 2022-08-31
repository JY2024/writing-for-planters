from PyQt5.QtGui import QTextDocument
from PyQt5.QtWidgets import QSizePolicy, QTextEdit

import collapsableBox


class BoxForStory(collapsableBox.CollapsableBox):
    """CollapsableBox with text edit"""
    def __init__(self, button_text, id):
        self.id = id
        self.text_edit = QTextEdit()
        self.init_ui()
        super().__init__(button_text, self.text_edit)

    def init_ui(self):
        """Initializes the UI for BoxForStory"""
        self.text_edit.setMaximumHeight(0)
        self.text_edit.setMinimumHeight(0)
        self.text_edit.setMaximumWidth(940)
        self.text_edit.setStyleSheet("background-color: rgb(243,240,240)")
        self.text_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def toggle_italics(self):
        """Toggles italics in QTextEdit for written work on and off"""
        self.text_edit.setFontItalic(not self.text_edit.fontItalic())

    def append_text(self, text):
        """Takes text: string, appends text to the current QTextEdit with focus"""
        if self.text_edit.hasFocus():
            self.text_edit.insertPlainText(text)
        else: # For comment box
            super().append_comment_text(text)

    def load_text(self, html_text, comments):
        """Takes html_text: string and comments: string, sets text and comments"""
        doc = QTextDocument()
        doc.setHtml(html_text)
        self.text_edit.setDocument(doc)
        self.comment_text_edit.setText(comments)

    def get_id(self):
        """Returns id of BoxForStory"""
        return self.id

    def get_written_work(self):
        """Returns BoxForStory's QTextEdit text containing text that is part of the written work"""
        return self.text_edit.toPlainText()

    def get_comments(self):
        """Returns BoxForStory's QTextEdit text containing comments"""
        return self.comment_text_edit.toPlainText()

    def to_html(self):
        """Returns BoxForStory's written work in HTML format"""
        return self.text_edit.toHtml()

    def set_writing(self, text):
        """Takes text: string, changes written work QTextEdit to contain text"""
        self.text_edit.clear()
        self.text_edit.setText(text)

    def set_text_color(self, color):
        """Takes color: QColor, sets the text in the current QTextEdit to color"""
        if self.text_edit.hasFocus():
            self.text_edit.setTextColor(color)
        else:
            self.comment_text_edit.setTextColor(color)

    def has_placeholder(self, action):
        """Takes action: string, returns whether this written work contains action keyword"""
        return action in self.get_written_work()