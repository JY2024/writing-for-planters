import designFunctions
from PyQt5.QtCore import QPropertyAnimation, QParallelAnimationGroup, QAbstractAnimation, QSize
from PyQt5.QtWidgets import (
    QVBoxLayout, QTextEdit, QWidget, QSizePolicy, QHBoxLayout, QStyle
)


class CollapsableBox(QWidget):
    def __init__(self, text, id):
        # Set up
        super().__init__()
        self.id = id

        self.text_edit = QTextEdit()
        self.comment_text_edit = QTextEdit()
        self.text_edit.setMaximumHeight(0)
        self.text_edit.setMinimumHeight(0)
        self.text_edit.setMaximumWidth(940)
        self.text_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.comment_text_edit.setMaximumWidth(self.text_edit.maximumWidth() * 0.25)
        self.comment_text_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        layout = QVBoxLayout(self)
        self.button = designFunctions.generate_button(text, checkable=True, size=QSize(900, 50))
        self.comment_button = designFunctions.generate_button(text="", checkable=True, size=QSize(40, 40))
        pixmapi = getattr(QStyle, "SP_FileDialogDetailedView")
        icon = self.style().standardIcon(pixmapi)
        self.comment_button.setIcon(icon)

        self.top_layout = QHBoxLayout()
        self.top_layout.addWidget(self.button)
        self.top_layout.addWidget(self.comment_button)
        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.addWidget(self.text_edit)
        self.bottom_layout.addWidget(self.comment_text_edit)
        layout.addLayout(self.top_layout)
        layout.addLayout(self.bottom_layout)

        # Animations
        content_height = self.text_edit.sizeHint().height()
        self.content_animation = QPropertyAnimation(self.text_edit, b"maximumHeight")
        self.content_animation.setDuration(500)
        self.content_animation.setStartValue(0)
        self.content_animation.setEndValue(content_height)

        content_width = self.text_edit.maximumWidth()
        self.comment_animation = QPropertyAnimation(self.text_edit, b"maximumWidth")
        self.comment_animation.setDuration(500)
        self.comment_animation.setStartValue(content_width)
        self.comment_animation.setEndValue(content_width * 0.75)

        self.button.clicked.connect(self.button_was_clicked)
        self.comment_button.clicked.connect(self.on_comment_button_clicked)

        self.setLayout(layout)

    def button_was_clicked(self):
        checked = self.get_checked()
        if checked:
            self.content_animation.setDirection(QAbstractAnimation.Forward)
        else:
            self.content_animation.setDirection(QAbstractAnimation.Backward)
        self.content_animation.start()

    def text(self):
        return self.button.text()

    def get_checked(self):
        return self.button.isChecked()

    def toggle_checked(self):
        self.button.setChecked(not self.button.isChecked())

    def set_text(self, text):
        self.button.setText(text)

    def get_id(self):
        return self.id

    def get_written_work(self):
        return self.text_edit.toPlainText()

    def set_writing(self, text):
        self.text_edit.clear()
        self.text_edit.setText(text)

    def on_comment_button_clicked(self):
        checked = self.comment_button.isChecked()
        if checked:
            self.comment_animation.setDirection(QAbstractAnimation.Forward)
        else:
            self.comment_animation.setDirection(QAbstractAnimation.Backward)
        self.comment_animation.start()
