from os import system
import PyQt6.QtCore as QtCore
from PyQt6.QtWidgets import QListWidgetItem,QTableWidgetItem

def add_to_list(list,item_name):
    item = QListWidgetItem()
    item.setText(item_name)
    list.addItem(item)

def add_to_table(table,id,name,category,raw_goods,system_id):
    row_pos = table.rowCount()
    table.insertRow(row_pos)
    col0 = QTableWidgetItem(str(id))
    col0.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
    col1 = QTableWidgetItem(name)
    col1.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
    col2 = QTableWidgetItem(category)
    col3 = QTableWidgetItem(raw_goods)
    col4 = QTableWidgetItem(system_id)
    table.setItem(row_pos , 0, col0)
    table.setItem(row_pos , 1, col1)
    table.setItem(row_pos , 2, col2)
    table.setItem(row_pos , 3, col3)
    table.setItem(row_pos , 4, col4)