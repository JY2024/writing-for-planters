from PyQt5.QtWidgets import QScrollArea, QWidget, QVBoxLayout, QDialog


class EditWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.mainLayout = QVBoxLayout()

        # Finish layout set up
        widget = QWidget()
        widget.setLayout(self.mainLayout)
        self.scroll = QScrollArea()
        self.scroll.setWidget(widget)
        self.scroll.setWidgetResizable(True)