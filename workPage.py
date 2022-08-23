from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QMainWindow, QWidget, QScrollArea, QLabel, QVBoxLayout, QPushButton

import customDialog
import partCreationWidget
import removableItemsHolder
import writingWindow
import partSummary
import designFunctions
import scrollableWindow


class WorkPage(scrollableWindow.ScrollableWindow):
    def __init__(self, title, tags, description):

        self.titleLabel = designFunctions.generate_label(title, font_size="40px", bold=True, alignment=Qt.AlignCenter)

        self.tagLabel = designFunctions.generate_label(tags, font_size="14px", border=True, size=QSize(800, 200),
                                                       background_color="white")
        self.descriptionLabel = designFunctions.generate_label(description, font_size="14px", border=True,
                                                               size=QSize(800, 200), background_color="white")
        self.addPartButton = QPushButton("Add Part")
        self.remove_button = designFunctions.generate_button("Remove Part", checkable=True)

        self.removable_items = removableItemsHolder.RemovableItemsHolder(self.remove_button,
                                                                         partCreationWidget.PartCreationWidget,
                                                                         partSummary.PartSummary,
                                                                         writingWindow.WritingWindow)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.titleLabel)
        self.mainLayout.addWidget(self.tagLabel)
        self.mainLayout.addWidget(self.descriptionLabel)
        self.mainLayout.addWidget(self.addPartButton)
        self.mainLayout.addWidget(self.remove_button)
        self.mainLayout.addWidget(self.removable_items)

        super().__init__(title, QSize(900, 700), self.mainLayout)
        
        self.addPartButton.clicked.connect(self.removable_items.on_create_clicked)
        self.remove_button.clicked.connect(self.removable_items.on_remove_clicked)

