def toggle_checkbox_visible(check_box):
    if check_box.isVisible():
        check_box.hide()
    else:
        check_box.show()

def is_checked(check_box):
    return check_box.isChecked()

def get_checkbox(item):
    return item.check_box