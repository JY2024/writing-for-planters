import draggableLabel
from PyQt5.QtWidgets import QScrollArea, QWidget, QVBoxLayout


class EditWindow(QWidget):
    def __init__(self, bulletPoints):
        super().__init__()

        self.setWindowTitle("Edit")

        self.mainLayout = QVBoxLayout()

        # Set up labels
        for bullet in bulletPoints:
            self.mainLayout.addWidget(draggableLabel.DraggableLabel(parent=self, text=bullet.get_text()))

        # Finish layout set up
        self.setLayout(self.mainLayout)
        self.scroll = QScrollArea()
        self.scroll.setWidget(self)
        self.scroll.setWidgetResizable(True)

    def on_mouse_release(self):
        order = self.sorted_children()
        for index, widget in enumerate(order):
            self.mainLayout.takeAt(index)
            self.mainLayout.insertWidget(index, widget)

    def sorted_children(self):
        labels = [self.mainLayout.itemAt(i).widget() for i in range(self.mainLayout.count())]
        return sorted(labels, key=lambda label: label.pos().y())