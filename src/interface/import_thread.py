import pandas as pd
from src.constants import COLUMN_NAMES
from src.errors import InvalidFileFormatError, NoCategoryError, ParserError
from src.import_files import export_excel
from src.interface.helper_functions import add_to_list, add_to_table
from src.parsers.ac_import import AC_Import
from PyQt6.QtCore import QThread, pyqtSignal
import os
from src.parsers.bc_import import BC_Import
from src.parsers.df_import import DF_Import
from src.parsers.gg_import import GG_Import
from src.parsers.hk_import import HK_Import
from src.parsers.sg_import import SG_Import

class ImportThread(QThread):
    """
    Import thread, handles all the functions related to when the user presses the import or export button
    """
    _signal = pyqtSignal(str)
    def __init__(self,filepath,import_list,nocat_list,args):
        """
        Init function for the importthread
        args:
            filepath: PyQT QLineEdit object where the user filepath/dir is listed
            import_list: PyQT QListWidget object, which lists the files imported
            nocat_list: PyQT QTableWidget object, which lists the imported items with no category/raw goods
            args: Dictionary with 2 boolean values, 'import' is if its import or export, 'load_file' is if the user selected a file or a directory
        """
        super(ImportThread, self).__init__()
        #Contains 'import' which is if user pressed import or export button and 'load_file' if user selected a file or a directory
        self.args = args
        #The object for the textline from the UI
        self.fp = filepath
        #Object to the import list on the UI
        self.import_list = import_list
        #Object to the no categories table on the UI
        self.nocat_list = nocat_list
        #How many lines have been added
        self.curadded = 0
        #Data currently parsed
        self.imported_lines = []
        #Index lists for imported lines where a no category error was found
        self.nocat_indexes = dict()
        #completed files
        self.completed_files = set()

        #Parsers available to be used
        self.parsers = [AC_Import(),BC_Import(),GG_Import(),DF_Import(),SG_Import(),HK_Import()]
        #self.parsers = [AC_Import()]

    def __del__(self):
        self.wait()

    def run(self):
        """
        Runs the thread
        """
        #Get filepath from the fp object from the UI
        filepath = self.fp.text()
        #Check if import was pressed
        if self.args['import']:
            #Check if the user selected a file or a directory
            if self.args['load_file']:
                self.import_file(filepath)
            else:
                self.import_dir(filepath)
        else:
            #update changes the user made in the no category table
            self.update_category_changes()

            #TODO Update the static lists

            #Remove the last entry in a row as it is just used for ID internally, if there is not more than 21 entries nothing is changed            
            for i in range(len(self.imported_lines)):
                if len(self.imported_lines[i]) > 21:
                    self.imported_lines[i] = self.imported_lines[i][:-1]
            #Create dataframe for export
            resdf = pd.DataFrame(self.imported_lines,columns = COLUMN_NAMES)
            try:
                #Export to excel
                export_excel(resdf,'renset.xlsx')
                #Emit to main view to unlock the buttons
                self._signal.emit(str(100))
            except PermissionError:
                #If file is open
                self._signal.emit('File is open')


    
    def import_file(self,filepath):
        """
        Imports and parses a xlsx and csv file. If a file is not valid for one of the parsers file is not parsed
        args:
            filepath: Path to file
        """
        #Find parser for file
        try:
            (length,parser) = self.load_file(self.parsers,filepath)

        except FileNotFoundError:
            self._signal.emit('File not found')
            return
        except InvalidFileFormatError:
            self._signal.emit('Invalid file format')
            return
        except ParserError:
            self._signal.emit('No parser for file found')
            return

        #Iterate over file contents
        for i in range(length):
            res = self.parse_line(parser,i)
            if res:
                self.imported_lines = self.imported_lines + res
                self.curadded += len(res)
            #Update progress bar
            prog = int(((i+1) / (length))*100)
            self._signal.emit(str(prog))


    def import_dir(self,dirpath):
        """
        Import and parses all files xlsx and csv files from a directory. If a file is not valid for one of the parsers 
        assigned in the constructor it skips it
        args:
            dirpath: Path to directory
        """

        #Get all files xlsx and csv filepaths
        files = self.get_files_from_dir(dirpath)
        #Get amount of files, using a number due to sending progress to progress bar
        num_files = len(files)
        for j in range(num_files):
            #Check if file is added already, if so skip to next file
            if files[j] in self.completed_files:
                self._signal.emit('Already imported %s' % files[j])
                continue
            
            #Find parser for file
            try:
                (length,parser) = self.load_file(self.parsers,files[j])

            except FileNotFoundError:
                self._signal.emit('File not found')
                return
            except InvalidFileFormatError:
                self._signal.emit('Invalid file format')
                return
            except ParserError:
                self._signal.emit('No parser for file found')
                return

            #Iterate over each row in the file
            for i in range(length):
                #Parse line
                res = self.parse_line(parser,i)
                if res:
                    self.imported_lines = self.imported_lines + res
                    self.curadded += len(res)
            self.completed_files.add(files[j])
            #Progress bar update
            prog = int(((j+1) / (num_files))*100)
            self._signal.emit(str(prog))
            add_to_list(self.import_list,files[j])

    def update_category_changes(self):
        """
        Checks the rows of the objects that were found to have no category during parsing. If a row is changed
        it updates the imported line values where the id is present
        """
        #Get amount of rows in the no category list
        amount_rows = self.nocat_list.rowCount()

        for i in range(amount_rows):
            #Get category and raw_goods fields
            category = self.nocat_list.item(i,2).text()
            raw_goods = self.nocat_list.item(i,3).text()

            #Check if they are changed
            if category != '' or raw_goods != '':
                #Grab the ID of the item
                index = self.nocat_list.item(i,0).text()
                #
                for val in self.nocat_indexes[index]:
                    row = self.imported_lines[val] 
                    #3 and 5 is the indexes for cat and rawgoods
                    row[3] = category
                    row[5] = raw_goods

    def parse_line(self,parser,index):
        """
        Parses a given index in the file loaded into the parser object
        args:
            parser: The parser object which is parsing the current file
            index: Int value of the index to parse
        returns:
            a array of arrays, where each sub array is one or more items that were parsed
            none if the line could not be parsed
        """
        try:
            line = parser.parse_line(index)
            return line
        except NoCategoryError:
            #If we fail we parse again where we return '' values in the category and raw_goods fields
            line = parser.parse_line(index,allow_nocat = True)
            #ID of the item is the last item of the row
            if line:
                id = str(line[0][-1])
                #If we already added an entry for an ID we dont create a new row but just add it to the index list
                if id in self.nocat_indexes:
                    self.nocat_indexes[id].append(self.curadded)
                else:
                    #Add the missing item as a row in the no categories table
                    add_to_table(self.nocat_list,line[0])
                    #Add ID to the index list so we know which line was added in the no category table
                    self.nocat_indexes[id] = [self.curadded]
            return line
        except ValueError:
            #print('test valueeror')
            return 
        except IndexError:
            return 

    def load_file(self,parsers,filepath):
        """
        Loads a xlsx or csv file, finds the parser assosiated with the file that can parse it. It loads the data into the parser selected
        args:
            parsers: List of parser objects
            filepath: String path to file
        returns:
            (length,parser) tuple, where length is an int of the length of data and parser is the parser that was found to be valid for the given file
        throws:
            ParserError: If no parser is valid for the file
        """
        for parser in parsers:
            try:
                length = parser.load_data(filepath)
                return (length,parser)
            except ParserError:
                pass
            except InvalidFileFormatError:
                pass
        #If no parser is found throw error
        raise ParserError()



    def get_files_from_dir(self,dirpath):
        """
        Takes a directory and returns all xlsx and csv files in that and any subdirectories
        args:
            dirpath: String path to the directory
        returns:
            List of string paths to all xlsx and csv files
        """
        allowed_extensions = ['.xlsx','.csv']
        if not os.path.isdir(dirpath):
            pass
        all_files = os.walk(dirpath)
        files_to_import = []

        for (dir,_,files) in all_files:
            #Remove non xlsx and csv files
            files = [ dir + '/' + file for file in files if file.endswith( tuple(allowed_extensions)) ]
            #Remove "opened" files
            files = [file for file in files if not '~$' in file]
            files_to_import = files_to_import + files
        return files_to_import