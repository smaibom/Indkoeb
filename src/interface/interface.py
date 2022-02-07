import sys
from PyQt6.QtWidgets import QApplication, QWidget,QVBoxLayout,QPushButton,QFileDialog,QLineEdit,QProgressBar,QTableWidget,QListWidget,QTableWidgetItem
from src.errors import InvalidFileFormatError,NoCategoryError,ParserError
from src.create_functions import create_button,create_textfield,create_drop_down
from src.interface.import_thread import ImportThread
from src.parsers.ac_import import AC_Import
from src.constants import AC
import PyQt6.QtCore as QtCore





class Example(QWidget):
    def __init__(self):
        super(Example, self).__init__()
        self.setWindowTitle('Import Excel')
        self.create_gui()
        self.show()

    
    def create_gui(self):
        self.pbar = QProgressBar(self)
        self.pbar.setValue(0)

        self.importbtn = QPushButton('Import')
        self.importbtn.clicked.connect(self.import_data)
        
        self.exportbtn = QPushButton('Export')
        self.exportbtn.clicked.connect(self.export_data)

        self.thread_args = dict()
        self.thread_args['import'] = True
        self.thread_args['load_file'] =  True
        self.thread_args['save_file_name'] = ''

        self.filepath = QLineEdit("Pick file or directory")
        self.filepath.setReadOnly(True)

        self.choosefilebutton = QPushButton('Pick file')
        self.choosefilebutton.clicked.connect(self.choose_file) 

        self.choosedirbutton = QPushButton('Pick dir')
        self.choosedirbutton.clicked.connect(self.choose_dir) 

        self.imported_list = QListWidget()

        self.missing_info_list = QTableWidget()
        self.missing_info_list.setColumnCount(5) 
        header0 = QTableWidgetItem('ID')
        header1 = QTableWidgetItem('Navn')
        header2 = QTableWidgetItem('Råvarekategori')
        header3 = QTableWidgetItem('Råvare')
        header4 = QTableWidgetItem('index')
        self.missing_info_list.setHorizontalHeaderItem(0,header0)
        self.missing_info_list.setHorizontalHeaderItem(1,header1)
        self.missing_info_list.setHorizontalHeaderItem(2,header2)
        self.missing_info_list.setHorizontalHeaderItem(3,header3)
        self.missing_info_list.setHorizontalHeaderItem(4,header4)
        self.missing_info_list.setColumnHidden(4,True)




        self.thread = ImportThread(self.filepath,self.imported_list,self.missing_info_list,self.thread_args)
        self.thread._signal.connect(self.signal_accept)
  
        self.errorbox = QLineEdit("")
        self.errorbox.setReadOnly(True)

        self.resize(600, 100)

        self.vbox = QVBoxLayout()

        self.vbox.addWidget(self.filepath)
        self.vbox.addWidget(self.choosefilebutton)
        self.vbox.addWidget(self.choosedirbutton)
        self.vbox.addWidget(self.pbar)
        self.vbox.addWidget(self.importbtn)
        self.vbox.addWidget(self.errorbox)
        self.vbox.addWidget(self.imported_list)
        self.vbox.addWidget(self.exportbtn)
        self.vbox.addWidget(self.missing_info_list)
        self.setLayout(self.vbox)


        

    def import_data(self):
        self.thread_args['import'] = True
        self.importbtn.setEnabled(False)
        self.exportbtn.setEnabled(False)
        self.thread.start()

    def export_data(self):
        (fp,_) = QFileDialog.getSaveFileName(self, 'Save File', filter = 'Excel Files(*.xlsx)')
        if fp != '': 
            self.thread_args['import'] = False
            self.thread_args['save_file_name'] = fp
            self.importbtn.setEnabled(False)
            self.exportbtn.setEnabled(False)
            self.thread.start()


    def signal_accept(self, msg):
        if not msg.isnumeric():
            self.errorbox.setText(msg)
            self.pbar.setValue(0)
            self.importbtn.setEnabled(True)
            self.exportbtn.setEnabled(True)
        else:
            self.pbar.setValue(int(msg))
            if self.pbar.value() == 100:
                self.importbtn.setEnabled(True)
                self.exportbtn.setEnabled(True)

    def choose_file(self):
        dialog = QFileDialog()
        (fp,_) = dialog.getOpenFileName(filter = 'Excel Files(*.xlsx *.csv)')
        if fp != '':
            self.filepath.setText(fp)
            self.thread_args['load_file'] = True

    def choose_dir(self):
        dialog = QFileDialog()
        dp = dialog.getExistingDirectory()
        if dp != '':
            self.filepath.setText(dp)
            self.thread_args['load_file'] = False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())