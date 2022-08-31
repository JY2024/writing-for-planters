from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLineEdit


class DraggableLabel(QLineEdit):
    """QLineEdit that can be moved around by the user"""
    def __init__(self, parent=None, text=None, id=None):
        super().__init__()
        self.setParent(parent)
        self.setText(text)
        self.id = id
        self.drag_start_pos = None

    def init_ui(self):
        """Initializes UI for DraggableLabel"""
        self.setFixedSize(200, 40)
        self.setStyleSheet("border: 1px solid black; background-color: white")
        self.textChanged.connect(self.on_text_changed)

    def mousePressEvent(self, event):
        """Takes event: QMouseEvent, changes cursor icon and allows this DraggableLabel to be moved"""
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self.setCursor(Qt.ClosedHandCursor)
            self.raise_()
            self.drag_start_pos = event.pos()

    def mouseMoveEvent(self, event):
        """Takes event: QMouseEvent, moves this DraggableLabel"""
        super().mouseMoveEvent(event)
        if self.drag_start_pos is not None:
            self.move(self.pos() + event.pos() - self.drag_start_pos)

    def mouseReleaseEvent(self, event):
        """Takes event: QMouseEvent, changes cursor icon and releases this DraggableLabel"""
        super().mouseReleaseEvent(event)
        self.setCursor(Qt.ArrowCursor)
        self.drag_start_pos = None
        self.parent().on_mouse_release()

    def on_text_changed(self):
        """Notifies the EditWindow that the text has changed, providing the text and the id"""
        self.parent().on_text_changed(self.text(), self.id)

    def get_id(self):
        """Returns id"""
        return self.id