import sys
import time
from PyQt6.QtWidgets import QApplication, QWidget,QMessageBox,QVBoxLayout,QPushButton,QLabel,QComboBox,QFileDialog,QLineEdit,QMainWindow,QProgressBar

from create_functions import create_button,create_textfield,create_drop_down
from ac_import import AC_Import
from constants import AC
from PyQt6.QtCore import QThread, pyqtSignal



"""
class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Import app'
        self.left = 10
        self.top = 10
        self.width = 1000
        self.height = 600
        self.parsers = {'ac' : AC_Import(AC)}
        self.initUI()


    def initUI(self):
        self.create_import_widgets()
        self.run_parser_button()
        self.show()

    def create_import_widgets(self):
        def pick_directory(text_field):
            dialog = QFileDialog()
            dir = dialog.getExistingDirectory()
            tf = text_field[0]
            if dir != '':
                text_field[0].setText(dir)

        tfx = 0
        tfy = 30
        tftext = ''
        readonly = True
        tf = create_textfield(self,tfx,tfy,tftext,readonly)
        tf.setMinimumWidth(250)

        
        bx = 100
        by = 100
        bname = 'pick dir' 
        btn = create_button(self,100,100,'pick dir',pick_directory,[tf])


    def run_parser_button(self):
        def run_parser(parser,filedir):

"""



        



class ImportThread(QThread):
    _signal = pyqtSignal(str)
    def __init__(self,filepath,parser):
        super(ImportThread, self).__init__()
        self.fp = filepath
        self.parser = parser
        self.parsers = {'ac' : AC_Import}

    def __del__(self):
        self.wait()

    def run(self):
        parser_type = self.parser.currentText()
        parser = self.parsers[parser_type]()
        filepath = self.fp.text()
        try:
            length = parser.load_data(filepath)
            for i in range(length):
                parser.import_line(i)
                prog = int((i / (length-1))*100)
                if i == (length-1):
                    self._signal.emit('Successfully imported %s lines' % length)
                else:
                    self._signal.emit(str(prog))
        except FileNotFoundError:
            self._signal.emit('File not found')
        except ValueError:
            self._signal.emit('Invalid file format')


class Example(QWidget):
    def __init__(self):
        super(Example, self).__init__()
        self.setWindowTitle('Import Excel')
        self.create_gui()
        self.show()

    
    def create_gui(self):
        self.pbar = QProgressBar(self)
        self.pbar.setValue(0)

        self.btn = QPushButton('Import')
        self.btn.clicked.connect(self.import_data)

        parserlabel = QLabel('Choose parser')

        self.pcb = QComboBox()
        self.pcb.addItem('ac')

        self.filepath = QLineEdit("Test")
        self.filepath.setReadOnly(True)
        self.choosefilebutton = QPushButton('Pick file')
        self.choosefilebutton.clicked.connect(self.choose_file) 

        self.errorbox = QLineEdit("")
        self.errorbox.setReadOnly(True)

        self.resize(600, 100)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(parserlabel)
        self.vbox.addWidget(self.pcb)
        self.vbox.addWidget(self.filepath)
        self.vbox.addWidget(self.choosefilebutton)
        self.vbox.addWidget(self.pbar)
        self.vbox.addWidget(self.btn)
        self.vbox.addWidget(self.errorbox)
        self.setLayout(self.vbox)


        

    def import_data(self):
        self.thread = ImportThread(self.filepath,self.pcb)
        self.thread._signal.connect(self.signal_accept)
        self.thread.start()
        self.btn.setEnabled(False)

    def signal_accept(self, msg):
        if not msg.isnumeric():
            self.errorbox.setText(msg)
            self.pbar.setValue(0)
            self.btn.setEnabled(True)
        else:
            self.pbar.setValue(int(msg))
            if self.pbar.value() == 99:
                self.pbar.setValue(0)
                self.btn.setEnabled(True)

    def choose_file(self):
        dialog = QFileDialog()
        (fp,_) = dialog.getOpenFileName()
        if fp != '':
            self.filepath.setText(fp)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
    #ex = App()
    #sys.exit(app.exec())