import designFunctions
from PyQt5.QtCore import QPropertyAnimation, QParallelAnimationGroup, QAbstractAnimation, QSize
from PyQt5.QtWidgets import (
    QVBoxLayout, QTextEdit, QWidget, QSizePolicy, QHBoxLayout, QStyle
)

class CollapsableBox(QWidget):
    def __init__(self, text, item):
        # Set up
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.item = item

        self.button = designFunctions.generate_button(text, checkable=True, size=QSize(900, 50))
        self.comment_button = designFunctions.generate_button(text="", checkable=True, size=QSize(40, 40))
        pixmapi = getattr(QStyle, "SP_FileDialogDetailedView")
        icon = self.style().standardIcon(pixmapi)
        self.comment_button.setIcon(icon)
        self.top_layout = QHBoxLayout()
        self.top_layout.addWidget(self.button)
        self.top_layout.addWidget(self.comment_button)

        self.comment_text_edit = QTextEdit()
        self.comment_text_edit.setMaximumHeight(0)
        self.comment_text_edit.setMinimumHeight(0)
        self.comment_text_edit.setMaximumWidth(0)
        self.comment_text_edit.setMinimumWidth(0)
        self.comment_text_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.addWidget(item)
        self.bottom_layout.addWidget(self.comment_text_edit)

        self.layout.addLayout(self.top_layout)
        self.layout.addLayout(self.bottom_layout)

        # Animations
        content_height = self.item.sizeHint().height()
        self.animation_group_vertical = QParallelAnimationGroup()
        self.animation_group_horizontal = QParallelAnimationGroup()
        self.content_animation_vertical = QPropertyAnimation(self.item, b"maximumHeight")
        self.content_animation_vertical.setDuration(500)
        self.content_animation_vertical.setStartValue(0)
        self.content_animation_vertical.setEndValue(content_height)

        content_width = self.item.maximumWidth()
        self.content_animation_horizontal = QPropertyAnimation(self.item, b"maximumWidth")
        self.content_animation_horizontal.setDuration(500)
        self.content_animation_horizontal.setStartValue(content_width)
        self.content_animation_horizontal.setEndValue(content_width * 0.75)

        self.comment_animation_vertical = QPropertyAnimation(self.comment_text_edit, b"maximumHeight")
        self.comment_animation_vertical.setDuration(500)
        self.comment_animation_vertical.setStartValue(0)
        self.comment_animation_vertical.setEndValue(content_height)

        comment_width = int(content_width * 0.25)
        self.comment_animation_horizontal = QPropertyAnimation(self.comment_text_edit, b"maximumWidth")
        self.comment_animation_horizontal.setDuration(500)
        self.comment_animation_horizontal.setStartValue(0)
        self.comment_animation_horizontal.setEndValue(comment_width)

        self.animation_group_vertical.addAnimation(self.content_animation_vertical)
        self.animation_group_vertical.addAnimation(self.comment_animation_vertical)
        self.animation_group_horizontal.addAnimation(self.content_animation_horizontal)
        self.animation_group_horizontal.addAnimation(self.comment_animation_horizontal)

        self.button.clicked.connect(self.button_was_clicked)
        self.comment_button.clicked.connect(self.on_comment_button_clicked)

        self.setLayout(self.layout)

    def button_was_clicked(self):
        checked = self.get_checked()
        if checked:
            self.animation_group_vertical.setDirection(QAbstractAnimation.Forward)
        else:
            self.animation_group_vertical.setDirection(QAbstractAnimation.Backward)
        self.animation_group_vertical.start()

    def text(self):
        return self.button.text()

    def get_checked(self):
        return self.button.isChecked()

    def toggle_checked(self):
        self.button.setChecked(not self.button.isChecked())

    def set_text(self, text):
        self.button.setText(text)

    def on_comment_button_clicked(self):
        checked = self.comment_button.isChecked()
        if checked:
            self.animation_group_horizontal.setDirection(QAbstractAnimation.Forward)
        else:
            self.animation_group_horizontal.setDirection(QAbstractAnimation.Backward)
        self.animation_group_horizontal.start()

    def append_text(self, text):
        self.comment_text_edit.insertPlainText(text)