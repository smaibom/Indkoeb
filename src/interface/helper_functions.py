import PyQt6.QtCore as QtCore
from PyQt6.QtWidgets import QListWidgetItem

def add_to_list(list,item_name):
    item = QListWidgetItem()
    item.setText(item_name)
    item.setFlags(item.flags() | QtCore.Qt.ItemFlag.ItemIsUserCheckable)
    item.setCheckState(QtCore.Qt.CheckState.Checked)
    list.addItem(item)
