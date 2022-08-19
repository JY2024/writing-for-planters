from PyQt5 import Qt
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QLabel, QPushButton


def generate_label(text="", background_color="white", font_size="20px", bold=False, border=False, size=QSize(1000, 50), alignment=Qt.AlignLeft):
    label = QLabel(text)
    return general_visual_setup(background_color, font_size, bold, border, size, alignment)

def generate_button(text="", background_color="white", font_size="20px", bold=False, border=False, size=QSize(1000, 50), alignment=Qt.AlignLeft, checkable=False):
    button = QPushButton(text)
    button.setCheckable(checkable)
    return general_visual_setup(background_color, font_size, bold, border, size, alignment)

def generate_text_edit(text="", size=QSize()):
    pass

def generate_line_edit(text="", ):
    pass

def general_visual_setup(widget, text="", background_color="white", font_size="20px", bold=False, border=False, size=QSize(1000, 50), alignment=Qt.AlignLeft):
    font = font_size if not bold else ("bold " + font_size)
    style_sheet = "background-color: " + background_color + "; font: " + font
    if border:
        style_sheet += "; border: 1px solid black"
    widget.setStyleSheet(style_sheet)
    widget.setFixedSize(size)
    widget.setAlignment(alignment)
    return widget

