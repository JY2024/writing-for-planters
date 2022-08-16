from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel


class DraggableLabel(QLabel):
    def __init__(self):
        super().__init__()

        self.setFixedSize(100, 20)
        self.drag_start_pos = None

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self.setCursor(Qt.ClosedHandCursor)
            self.raise_()
            self.drag_start_pos = event.pos()
