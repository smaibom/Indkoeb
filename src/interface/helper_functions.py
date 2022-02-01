import PyQt6.QtCore as QtCore
from PyQt6.QtWidgets import QListWidgetItem,QTableWidgetItem

def add_to_list(list,item_name):
    item = QListWidgetItem()
    item.setText(item_name)
    item.setFlags(item.flags() | QtCore.Qt.ItemFlag.ItemIsUserCheckable)
    item.setCheckState(QtCore.Qt.CheckState.Checked)
    list.addItem(item)

def add_to_table(table,row):
    row_pos = table.rowCount()
    table.insertRow(row_pos)
    col0 = QTableWidgetItem(str(row[-1]))
    col0.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
    col1 = QTableWidgetItem(row[7])
    col1.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
    col2 = QTableWidgetItem(row[3])
    col3 = QTableWidgetItem(row[5])
    table.setItem(row_pos , 0, col0)
    table.setItem(row_pos , 1, col1)
    table.setItem(row_pos , 2, col2)
    table.setItem(row_pos , 3, col3)