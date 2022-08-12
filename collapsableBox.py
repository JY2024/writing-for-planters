from PyQt5.QtCore import QPropertyAnimation, QParallelAnimationGroup, QAbstractAnimation, QSize
from PyQt5.QtWidgets import (
    QVBoxLayout, QPushButton, QTextEdit, QWidget, QSizePolicy
)


class CollapsableBox(QWidget):
    def __init__(self, text):
        # Set up
        super().__init__()

        self.textEdit = QTextEdit()
        self.textEdit.setMaximumHeight(0)
        self.textEdit.setMinimumHeight(0)
        self.textEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.animation_group = QParallelAnimationGroup(self)

        layout = QVBoxLayout(self)
        self.button = QPushButton(text)
        self.button.setCheckable(True)
        self.button.setChecked(False)
        layout.addWidget(self.button)
        layout.addWidget(self.textEdit)

        # Animation
        content_height = self.textEdit.sizeHint().height()
        self.content_animation = QPropertyAnimation(self.textEdit, b"maximumHeight")
        self.content_animation.setDuration(500)
        self.content_animation.setStartValue(0)
        self.content_animation.setEndValue(content_height)

        self.button.clicked.connect(self.button_was_clicked)

        self.setLayout(layout)

    def button_was_clicked(self):
        checked = self.button.isChecked()
        if checked:
            self.content_animation.setDirection(QAbstractAnimation.Forward)
        else:
            self.content_animation.setDirection(QAbstractAnimation.Backward)
        self.content_animation.start()
