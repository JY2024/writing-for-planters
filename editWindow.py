from PyQt5.QtWidgets import QScrollArea, QWidget, QVBoxLayout


class EditWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Edit")

        self.mainLayout = QVBoxLayout()

        # Finish layout set up
        self.setLayout(self.mainLayout)
        self.scroll = QScrollArea()
        self.scroll.setWidget(self)
        self.scroll.setWidgetResizable(True)