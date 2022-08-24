import draggableLabel
from PyQt5.QtWidgets import QScrollArea, QWidget, QVBoxLayout


class EditWindow(QWidget):
    def __init__(self, bullet_points):
        super().__init__()

        self.setWindowTitle("Edit")

        self.main_layout = QVBoxLayout()
        self.bullets = bullet_points

        # Set up labels
        for bullet in bullet_points:
            label = draggableLabel.DraggableLabel(parent=self, text=bullet.get_text(), id=bullet.get_id())
            self.main_layout.addWidget(label)

        # Finish layout set up
        self.setLayout(self.main_layout)
        self.scroll = QScrollArea()
        self.scroll.setWidget(self)
        self.scroll.setWidgetResizable(True)

    def on_mouse_release(self):
        order = self.sorted_children()
        for index, widget in enumerate(order):
            self.main_layout.takeAt(index)
            self.main_layout.insertWidget(index, widget)

    def sorted_children(self):
        labels = [self.main_layout.itemAt(i).widget() for i in range(self.main_layout.count())]
        return sorted(labels, key=lambda label: label.pos().y())

    def on_text_changed(self, updated_text, changed_id):
        bullet = next(x for x in self.bullets if x.get_id() == changed_id)
        bullet.set_text(updated_text)
        bullet.set_box_text(updated_text)