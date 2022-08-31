from PyQt5.QtWidgets import QScrollArea, QVBoxLayout, QWidget

import draggableLabel


class EditWindow(QWidget):
    """QWidget to assist in editing/reordering BulletPoints"""
    def __init__(self, bullet_points):
        super().__init__()
        self.bullets = bullet_points
        self.main_layout = QVBoxLayout()
        self.scroll = QScrollArea()
        self.init_ui()

    def init_ui(self):
        """Initializes UI for EditWindow"""
        self.setWindowTitle("Edit")
        for bullet in self.bullets:
            label = draggableLabel.DraggableLabel(parent=self, text=bullet.get_text(), id=bullet.get_id())
            self.main_layout.addWidget(label)
        self.setLayout(self.main_layout)
        self.scroll.setWidget(self)
        self.scroll.setWidgetResizable(True)

    def sorted_children(self):
        """Returns DraggableLabels sorted by y position"""
        labels = [self.main_layout.itemAt(i).widget() for i in range(self.main_layout.count())]
        return sorted(labels, key=lambda label: label.pos().y())

    def on_mouse_release(self):
        """Handles mouse release event by reordering DraggableLabels in this EditWindow layout"""
        order = self.sorted_children()
        for index, widget in enumerate(order):
            self.main_layout.takeAt(index)
            self.main_layout.insertWidget(index, widget)

    def on_text_changed(self, updated_text, changed_id):
        """Takes updated_text: string, changed_id: int, updates the matching BulletPoint text and BoxForStory text"""
        bullet = next(x for x in self.bullets if x.get_id() == changed_id)
        bullet.set_button_text(updated_text)
        bullet.set_box_text(updated_text)