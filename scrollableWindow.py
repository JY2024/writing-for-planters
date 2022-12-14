from PyQt5.QtWidgets import QMainWindow, QScrollArea, QWidget


class ScrollableWindow(QMainWindow):
    """QMainWindow with scrolling window"""
    def __init__(self, window_title, window_size, main_layout):
        super().__init__()
        self.setWindowTitle(window_title)
        self.setFixedSize(window_size)
        self.setStyleSheet("background-color: rgb(232,227,210);")

        widget = QWidget()
        widget.setLayout(main_layout)

        self.scroll = QScrollArea()
        self.scroll.setWidget(widget)
        self.scroll.setWidgetResizable(True)
        self.setCentralWidget(self.scroll)