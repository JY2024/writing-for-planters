import designFunctions

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QCheckBox, QVBoxLayout


class PartSummary(QWidget):
    def __init__(self, parent, title, synopsis, part_num):
        super().__init__()
        self.my_parent = parent
        self.title = title

        self.setMinimumSize(QSize(500, 300))
        self.setMaximumSize(QSize(500, 300))

        self.top_layout = QHBoxLayout()
        self.title_button = designFunctions.generate_button(
            "Part " + str(part_num) + ": " + title, bold=True, border=True, size=QSize(400, 50),
            background_color="white"
        )
        self.top_layout.addWidget(self.title_button)
        # Completion status
        self.check_box = QCheckBox()
        self.check_box.hide()
        self.top_layout.addWidget(self.check_box)
        self.synopsis_label = designFunctions.generate_label(synopsis, font_size="14px", border=True,
                                                            background_color="white", size=QSize(400, 200))

        self.main_layout = QVBoxLayout()

        self.main_layout.addLayout(self.top_layout)
        self.main_layout.addWidget(self.synopsis_label)
        self.setLayout(self.main_layout)

        self.title_button.clicked.connect(self.on_title_clicked)

    def on_title_clicked(self):
        self.my_parent.open_part(self.title)