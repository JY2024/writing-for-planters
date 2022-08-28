from PyQt5.QtWidgets import QGroupBox, QGridLayout

import collapsableBox
import designFunctions


class BoxForInfo(collapsableBox.CollapsableBox):
    def __init__(self):
        self.add_button = designFunctions.generate_button("Insert New Media")
        self.media_box = QGroupBox("Inspiration")
        self.media_layout = QGridLayout()
        self.media_box.setLayout(self.media_layout)
        self.media_layout.addWidget(self.add_button)

        super().__init__("Inspiration", self.media_box)

        self.add_button.clicked.connect(self.on_add)

    def on_add(self):
        pass


