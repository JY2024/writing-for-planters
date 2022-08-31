"""Common QCheckbox-related functions"""
def is_checked(check_box):
    """Takes check_box: QCheckBox, returns whether check_box is checked"""
    return check_box.isChecked()

def get_checkbox(item):
    """Takes item: type that has a QCheckBox, returns the item's QCheckBox"""
    return item.check_box

def toggle_checkbox_visible(check_box):
    """Takes check_box: QCheckBox, toggles the check_box's checked state"""
    if check_box.isVisible():
        check_box.hide()
    else:
        check_box.show()