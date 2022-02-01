from src.errors import InvalidFileFormatError, NoCategoryError, ParserError
from src.interface.helper_functions import add_to_list
from src.parsers.ac_import import AC_Import
from PyQt6.QtCore import QThread, pyqtSignal
import os
from src.parsers.bc_import import BC_Import
from src.parsers.df_import import DF_Import
from src.parsers.gg_import import GG_Import
from src.parsers.hk_import import HK_Import
from src.parsers.sg_import import SG_Import

class ImportThread(QThread):
    _signal = pyqtSignal(str)
    def __init__(self,filepath,is_file,import_list):
        super(ImportThread, self).__init__()
        self.fp = filepath
        self.import_list = import_list
        self.completed = dict()
        self.is_file = is_file
        #self.parsers = [AC_Import(),BC_Import(),GG_Import(),DF_Import(),SG_Import()]
        self.parsers = [HK_Import()]

    def __del__(self):
        self.wait()

    def run(self):
        filepath = self.fp.text()
        if self.is_file.isChecked():
            try:
                res = self.load_file(self.parsers,filepath)
                if res:
                    (length,parser) = res
                else:
                    self._signal.emit('No parser for file found')
                    return
            except FileNotFoundError:
                self._signal.emit('File not found')
                return
            except InvalidFileFormatError:
                self._signal.emit('Invalid file format')
                return
            imported = 0
            for i in range(length):
                res = self.parse_line(parser,i)
                if res:
                    imported += len(res)
                prog = int((i / (length-1))*100)
                if i == (length-1):
                    self._signal.emit('Successfully imported %s lines' % imported)
                else:
                    self._signal.emit(str(prog))
        else:
            files = self.get_files_from_dir(filepath)
            try:
                imported = 0
                num_files = len(files)
                for j in range(num_files):
                    if files[j] in self.completed:
                        self._signal.emit('Already imported %s' % files[j])
                        continue
                    imported_lines = []
                    res = self.load_file(self.parsers,files[j])
                    if res:
                        (length,parser) = res
                    else:
                        self._signal.emit('No parser for %s found' % files[j])
                        continue
                    for i in range(length):
                        res = self.parse_line(parser,i)
                        if res:
                            imported += len(res)
                            imported_lines = imported_lines + res
                    prog = int((j / (num_files-1))*100)
                    self._signal.emit('Successfully imported %s' % files[j])
                    if j == (num_files-1):
                        self._signal.emit('Successfully imported %s lines' % imported)
                    else:
                        self._signal.emit(str(prog))
                    add_to_list(self.import_list,files[j])
                    self.completed[files[j]] = imported_lines

                #self.import_dir(parser,filepath)
            except FileNotFoundError:
                self._signal.emit('File not found')
                return
            except InvalidFileFormatError:
                self._signal.emit('Invalid file format')
                return
            except ParserError:
                self._signal.emit('Excel file could not be read by given parser')
                return



        
        
    def parse_line(self,parser,index):
        try:
            line = parser.parse_line(index)
            return line
        except NoCategoryError:
            print('test nocat error')
            return  #TODO Handle later
        except ValueError:
            #Nothing for now
            print('test valueeror')
            return 
        except IndexError:
            self._signal.emit('Excel file could not be read by given parser')
            return

    def load_file(self,parsers,filepath):
        for parser in parsers:
            try:
                print(filepath)
                length = parser.load_data(filepath)
                return (length,parser)
            except ParserError:
                pass
            except InvalidFileFormatError:
                pass
        

    
    def import_file(self,parser,length):
        imported = 0
        for i in range(length):
            try:
                parser.parse_line(i)
                imported += 1
            except NoCategoryError:
                print('test nocat error')
                pass #TODO Handle later
            except ValueError:
                #Nothing for now
                print('test valueeror')
                pass
            except IndexError:
                self._signal.emit('Excel file could not be read by given parser')
                return
        return imported

    def get_files_from_dir(self,dirpath):
        allowed_extensions = ['.xlsx','.csv']
        if not os.path.isdir(dirpath):
            pass
        all_files = os.walk(dirpath)
        files_to_import = []
        for (dir,_,files) in all_files:
            files = [ dir + '/' + file for file in files if file.endswith( tuple(allowed_extensions)) ]
            files = [file for file in files if not '~$' in file]
            files_to_import = files_to_import + files
        return files_to_import