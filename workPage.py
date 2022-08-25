from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QVBoxLayout, QPushButton

import partCreationWidget
import removableItemsHolder
import writingWindow
import partSummary
import designFunctions
import scrollableWindow


class WorkPage(scrollableWindow.ScrollableWindow):
    def __init__(self, title, tags, description, folder_path):
        self.my_file = open(title + ".txt", "w")
        self.file_path = None
        self.folder_path = folder_path

        self.save_button = designFunctions.generate_button("Save")
        self.title_label = designFunctions.generate_label(title, font_size="40px", bold=True, alignment=Qt.AlignCenter)

        self.tag_label = designFunctions.generate_label(tags, font_size="14px", border=True, size=QSize(800, 200),
                                                       background_color="white")
        self.description_label = designFunctions.generate_label(description, font_size="14px", border=True,
                                                               size=QSize(800, 200), background_color="white")
        self.add_part_button = QPushButton("Add Part")
        self.remove_button = designFunctions.generate_button("Remove Part", checkable=True)

        self.removable_items = removableItemsHolder.RemovableItemsHolder(self.remove_button,
                                                                         partCreationWidget.PartCreationWidget,
                                                                         partSummary.PartSummary,
                                                                         writingWindow.WritingWindow)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.save_button)
        self.mainLayout.addWidget(self.title_label)
        self.mainLayout.addWidget(self.tag_label)
        self.mainLayout.addWidget(self.description_label)
        self.mainLayout.addWidget(self.add_part_button)
        self.mainLayout.addWidget(self.remove_button)
        self.mainLayout.addWidget(self.removable_items)

        super().__init__(title, QSize(900, 700), self.mainLayout)
        
        self.add_part_button.clicked.connect(self.removable_items.on_create_clicked)
        self.remove_button.clicked.connect(self.removable_items.on_remove_clicked)
        self.save_button.clicked.connect(self.on_save)

    def set_tags(self, text):
        self.tag_label.setText(text)

    def set_description(self, text):
        self.description_label.setText(text)

    def gather_text(self, parts):
        pass

    def on_save(self):
        text = self.gather_text(self.removable_items.get_parts())
        if self.file_path == None:
            pass
        else:
            pass


