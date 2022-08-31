from PyQt5.QtCore import QAbstractAnimation, QParallelAnimationGroup, QPropertyAnimation, QSize
from PyQt5.QtWidgets import QHBoxLayout, QSizePolicy, QStyle, QTextEdit, QVBoxLayout, QWidget

import designFunctions


class CollapsableBox(QWidget):
    """Box containing a widget and comment box"""
    def __init__(self, text, item):
        self.item = item
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.top_layout = QHBoxLayout()
        self.bottom_layout = QHBoxLayout()
        self.button = designFunctions.generate_button(text, checkable=True, size=QSize(900, 50))
        self.comment_button = designFunctions.generate_button(text="", checkable=True, size=QSize(40, 40))
        self.comment_text_edit = QTextEdit()
        self.init_ui()

        self.animation_group_vertical = QParallelAnimationGroup()
        self.animation_group_horizontal = QParallelAnimationGroup()
        self.content_animation_vertical = QPropertyAnimation(self.item, b"maximumHeight")
        self.content_animation_horizontal = QPropertyAnimation(self.item, b"maximumWidth")
        self.comment_animation_vertical = QPropertyAnimation(self.comment_text_edit, b"maximumHeight")
        self.comment_animation_horizontal = QPropertyAnimation(self.comment_text_edit, b"maximumWidth")

        self.init_animations()

    def init_ui(self):
        """Initializes UI for CollapsableBox"""
        pixmapi = getattr(QStyle, "SP_FileDialogDetailedView")
        icon = self.style().standardIcon(pixmapi)
        self.comment_button.setIcon(icon)
        self.comment_button.setStyleSheet("background-color: rgb(196,235,196)")

        self.comment_text_edit.setStyleSheet("background-color: rgb(243,240,240)")
        self.comment_text_edit.setMaximumHeight(0)
        self.comment_text_edit.setMinimumHeight(0)
        self.comment_text_edit.setMaximumWidth(0)
        self.comment_text_edit.setMinimumWidth(0)
        self.comment_text_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.top_layout.addWidget(self.button)
        self.top_layout.addWidget(self.comment_button)
        self.bottom_layout.addWidget(self.item)
        self.bottom_layout.addWidget(self.comment_text_edit)

        self.layout.addLayout(self.top_layout)
        self.layout.addLayout(self.bottom_layout)

        self.button.clicked.connect(self.on_text_button_clicked)
        self.comment_button.clicked.connect(self.on_comment_button_clicked)

        self.setLayout(self.layout)

    def init_animations(self):
        """Initializes animations for CollapsableBox"""
        content_height = self.item.sizeHint().height()
        content_width = self.item.maximumWidth()
        comment_width = int(content_width * 0.25)

        for animation in [self.content_animation_vertical, self.content_animation_horizontal,
                          self.comment_animation_vertical, self.comment_animation_horizontal]:
            animation.setDuration(500)

        self.content_animation_vertical.setStartValue(0) # Expand
        self.content_animation_vertical.setEndValue(content_height)
        self.comment_animation_vertical.setStartValue(0) # Expand
        self.comment_animation_vertical.setEndValue(content_height)
        self.content_animation_horizontal.setStartValue(content_width) # Shrink
        self.content_animation_horizontal.setEndValue(content_width * 0.75)
        self.comment_animation_horizontal.setStartValue(0) # Expand
        self.comment_animation_horizontal.setEndValue(comment_width)

        self.animation_group_vertical.addAnimation(self.content_animation_vertical)
        self.animation_group_vertical.addAnimation(self.comment_animation_vertical)
        self.animation_group_horizontal.addAnimation(self.content_animation_horizontal)
        self.animation_group_horizontal.addAnimation(self.comment_animation_horizontal)

    def on_text_button_clicked(self):
        """Sets the appropriate direction for collapsing/expanding animation of box and plays animation"""
        checked = self.get_checked()
        if checked:
            self.animation_group_vertical.setDirection(QAbstractAnimation.Forward) # Expand
        else:
            self.animation_group_vertical.setDirection(QAbstractAnimation.Backward) # Collapse
        self.animation_group_vertical.start()

    def on_comment_button_clicked(self):
        """Sets the appropriate direction for collapsing/expanding animation of comment box and plays animation"""
        checked = self.comment_button.isChecked()
        if checked:
            self.animation_group_horizontal.setDirection(QAbstractAnimation.Forward) # Expand
        else:
            self.animation_group_horizontal.setDirection(QAbstractAnimation.Backward) # Collapse
        self.animation_group_horizontal.start()

    def get_comment(self):
        """Returns comment text"""
        return self.comment_text_edit.toPlainText()

    def set_comment(self, text):
        """Takes text: string, sets comment text"""
        self.comment_text_edit.setText(text)

    def append_comment_text(self, text):
        """Takes text: string, appends text to comment text edit"""
        self.comment_text_edit.insertPlainText(text)

    def get_button_text(self):
        """Returns button text"""
        return self.button.text()

    def set_button_text(self, text):
        """Takes text: string, sets button text"""
        self.button.setText(text)

    def get_checked(self):
        """Returns whether the button is checked"""
        return self.button.isChecked()

    def toggle_checked(self):
        """Toggles checked state of button"""
        self.button.setChecked(not self.button.isChecked())