from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLineEdit


class DraggableLabel(QLineEdit):
    def __init__(self, parent=None, text=None, id=None):
        super().__init__()
        self.id = id

        self.setParent(parent)
        self.setFixedSize(200, 40)
        self.setText(text)
        self.setStyleSheet("border: 1px solid black; background-color: white")
        self.drag_start_pos = None

        self.textChanged.connect(self.on_text_changed)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self.setCursor(Qt.ClosedHandCursor)
            self.raise_()
            self.drag_start_pos = event.pos()

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if self.drag_start_pos is not None:
            self.move(self.pos() + event.pos() - self.drag_start_pos)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.setCursor(Qt.ArrowCursor)
        self.drag_start_pos = None
        self.parent().on_mouse_release()

    def on_text_changed(self):
        self.parent().on_text_changed(self.text(), self.id)

    def get_id(self):
        return self.id