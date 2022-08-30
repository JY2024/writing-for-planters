from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QTextDocument
from PyQt5.QtWidgets import QLabel, QPushButton, QTextEdit


def generate_label(text="", background_color="light grey", font_size="20px", bold=False, border=False,
                   size=QSize(870, 50), alignment=Qt.AlignLeft):
    label = QLabel(text)
    return general_visual_setup(label, background_color, font_size, bold, border, size, alignment)

def generate_button(text="", background_color="rgb(209,192,123)", font_size="15px", bold=False, border=False,
                    size=QSize(200, 25), checkable=False):
    button = QPushButton(text)
    button.setCheckable(checkable)
    return general_visual_setup(button, background_color, font_size, bold, border, size, None)

def generate_textEdit(doc=QTextDocument(""), background_color="rgb(233,227,227)", font_size="20px", bold=False, border=False,
                      size=QSize(870, 50), alignment=Qt.AlignLeft, read_only=False):
    text_edit = QTextEdit()
    text_edit.setDocument(doc)
    text_edit.setReadOnly(read_only)
    return general_visual_setup(text_edit, background_color, font_size, bold, border, size, alignment)

def general_visual_setup(widget, background_color, font_size, bold, border, size, alignment):
    font = font_size if not bold else ("bold " + font_size)
    style_sheet = "background-color: " + background_color + "; font: " + font
    if border:
        style_sheet += "; border: 1px solid black"
    widget.setStyleSheet(style_sheet)
    widget.setFixedSize(size)
    if alignment != None:
        widget.setAlignment(alignment)
    return widget

