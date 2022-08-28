from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGroupBox, QGridLayout, QVBoxLayout, QLabel, QFileDialog

import collapsableBox
import customDialog
import designFunctions
import scrollableWindow

class BoxForInfo(collapsableBox.CollapsableBox):
    def __init__(self):
        self.add_button = designFunctions.generate_button("Insert New Media")
        self.media_box = QGroupBox("Inspiration")
        self.media_layout = QGridLayout()
        self.media_box.setLayout(self.media_layout)
        self.media_layout.addWidget(self.add_button)

        super().__init__("Inspiration", self.media_box)

        self.media = {}
        self.popup = MediaSelectionPopup(self)
        self.popup.hide()

        self.add_button.clicked.connect(self.on_add)

    def on_add(self):
        self.popup.show()

    def add_media(self, media):
        pass

class MediaSelectionPopup(scrollableWindow.ScrollableWindow):
    def __init__(self, parent):
        self.parent = parent
        self.main_layout = QVBoxLayout()
        self.image_button = designFunctions.generate_button("Image")
        self.audio_button = designFunctions.generate_button("Audio")
        self.text_button = designFunctions.generate_button("Text")

        self.main_layout.addWidget(self.image_button)
        self.main_layout.addWidget(self.audio_button)
        self.main_layout.addWidget(self.text_button)

        super().__init__("Add Media", QSize(300, 200), self.main_layout)

        self.image_button.clicked.connect(self.on_image)
        self.audio_button.clicked.connect(self.on_audio)
        self.text_button.clicked.connect(self.on_text)

    def select_file(self, filter):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setFilter(filter)
        file_name = dlg.getOpenFileName()
        return file_name

    def on_image(self):
        label = QLabel()
        file_name = self.select_file("Image files (*.jpg *.png *.jpeg)")
        pixmap = QPixmap(file_name)
        label.setPixmap(pixmap)
        label.resize(pixmap.width(), pixmap.height())
        self.parent.add_media(label)

    def on_audio(self):
        dlg = customDialog.CustomDialog(

        )
        dlg.exec()

    def on_text(self):
        pass