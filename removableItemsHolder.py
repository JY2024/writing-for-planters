from PyQt5.QtWidgets import QGroupBox

class RemovableItemsHolder(QGroupBox):
    def __init__(self, create_button, remove_button, edit_button):
        super().__init__()

