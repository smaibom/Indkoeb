from PyQt6.QtWidgets import QApplication, QWidget,QMessageBox,QPushButton,QLabel,QComboBox,QFileDialog,QLineEdit

def create_drop_down(window,x,y,values):
    cb = QComboBox(window)
    cb.move(x,y)
    for value in values:
        cb.addItem(value)
    return cb

def create_button(window,x,y,text,func,func_args):
    btn = QPushButton(window)
    btn.setText(text)
    btn.move(x,y)
    btn.clicked.connect(lambda: func(func_args))
    return btn

def create_textfield(window,x,y,text,readonly):
    tf = QLineEdit(window)
    tf.setText(text)
    tf.move(x,y)
    tf.setReadOnly(readonly)
    return tf