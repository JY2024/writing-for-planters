from PyQt5.QtWidgets import QMainWindow, QWidget, QScrollArea


class ScrollableWindow(QMainWindow):
    def __init__(self, window_title, window_size, main_layout):
        super().__init__()

        self.setWindowTitle(window_title)
        self.setFixedSize(window_size)

        widget = QWidget()
        widget.setLayout(main_layout)
        self.scroll = QScrollArea()
        self.scroll.setWidget(widget)
        self.scroll.setWidgetResizable(True)
        self.setCentralWidget(self.scroll)



