import pandas as pd
from src.constants import CATEGORY_FILE_PATH, CATEGORY_INDEX, COLUMN_NAMES, NAME_INDEX, RAW_GOODS_INDEX
from src.errors import InvalidFileFormatError, NoCategoryError, ParserError
from src.excel_file_functions import export_excel, get_excel_sheet_names, write_sheets_to_excel_file
from src.interface.helper_functions import add_to_list, add_to_table
from PyQt6.QtCore import QThread, pyqtSignal
import os
from src.parsers import EM_Import,AC_Import,BC_Import,CBP_Import,DF_Import,GG_Import,HK_Import,SG_Import

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
        self.parsers = {'ac' : AC_Import(),'bc' : BC_Import(),'gg' : GG_Import(), 'df' :DF_Import(),
                        'sg' : SG_Import(), 'hk' : HK_Import(), 'cbp' : CBP_Import(), 'em' : EM_Import()}
        #self.parsers = []

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
            #Start progress bar
            self._signal.emit('0')

            #Check if the user selected a file or a directory
            if self.args['load_file']:
                self.import_file(filepath)
            else:
                self.import_dir(filepath)
        else:
            #update changes the user made in the no category table
            if len(self.imported_lines) == 0:
                self._signal.emit('No imported files')
                return
            changes = self.update_category_changes()

            #Remove the last entry in a row as it is just used for ID internally, if there is not more than 21 entries nothing is changed            
            for i in range(len(self.imported_lines)):
                if len(self.imported_lines[i]) > 21:
                    self.imported_lines[i] = self.imported_lines[i][:-1]
            #Create dataframe for export
            resdf = pd.DataFrame(self.imported_lines,columns = COLUMN_NAMES)
            try:
                #Export to excel
                fp = self.args['save_file_name']
                export_excel(resdf,fp)
                if changes:
                    self.update_category_file()
                #Emit to main view to unlock the buttons
                self._signal.emit("Finished exporting file")
            except PermissionError:
                #If file is open
                self._signal.emit('File is open')


    
    def import_file(self,filepath):
        """
        Imports and parses a xlsx and csv file. If a file is not valid for one of the parsers file is not parsed
        args:
            filepath: Path to file
        """
        filename = filepath.split('/')[-1]
        if filename in self.completed_files:
            self._signal.emit('Already imported %s' % filepath)
            return

        try:
            sheets = get_excel_sheet_names(filepath)
        except ValueError:
            #Just for csv file handling
            sheets = [None]
        except FileNotFoundError:
            self._signal.emit('No file selected')
            return
            
        is_used = False
        #To throttle the status bar
        prev_status_prog = 0
        for j in range(len(sheets)):
            try:
                #Find parser for file
                (length,parser) = self.load_file(self.parsers,filepath,sheets[j])
            except FileNotFoundError:
                self._signal.emit('File not found')
                return
            except InvalidFileFormatError:
                self._signal.emit('Invalid file format')
                return
            except ParserError:
                #Make sure status bar updates if sheet is bad
                prev_status_prog = int(((j+1)/len(sheets))*100)
                self._signal.emit(str(prev_status_prog))
                continue
            is_used = True
            #Iterate over file contents
            for i in range(length):
                res = self.parse_line(parser,i)
                if res:
                    self.imported_lines = self.imported_lines + res
                    self.curadded += len(res)
                #Update progress bar, TODO: Throttle this a bit as sending every line lags the UI
                prog_sheets = j/len(sheets)
                prog_file = ((i+1)/length)/len(sheets)
                prog = int((prog_sheets+prog_file)*100)
                if prog > prev_status_prog:
                    self._signal.emit(str(prog))
                prev_status_prog = prog
        if is_used:
            add_to_list(self.import_list,filename)
            self.completed_files.add(filename)
        else:
            self._signal.emit('No parser for file found')

        

    


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
            filename = files[j].split('/')[-1]
            #Check if file is added already, if so skip to next file
            if filename in self.completed_files:
                continue
            
            #Find parser for file
            is_used = False
            try:
                sheets = get_excel_sheet_names(files[j])
            except ValueError:
                #Just for csv file handling
                sheets = [None]
            #TODO Add more error handling here

            for sheet in sheets:
                try:
                    (length,parser) = self.load_file(self.parsers,files[j],sheet)

                except FileNotFoundError:
                    self._signal.emit('File not found')
                    return
                except InvalidFileFormatError:
                    self._signal.emit('Invalid file format')
                    return
                except ParserError:
                    continue
                is_used = True
        
                #Iterate over each row in the file
                for i in range(length):
                    #Parse line
                    res = self.parse_line(parser,i)
                    if res:
                        self.imported_lines = self.imported_lines + res
                        self.curadded += len(res)
                #Progress bar update
                prog = int(((j+1) / (num_files))*100)
                self._signal.emit(str(prog))
            if is_used:
                self.completed_files.add(filename)
                add_to_list(self.import_list,filename)
        self._signal.emit('Finished importing files')

    def update_category_changes(self):
        """
        Checks the rows of the objects that were found to have no category during parsing. If a row is changed
        it updates the imported line values where the id is present
        """
        #Get amount of rows in the no category list
        amount_rows = self.nocat_list.rowCount()
        is_changes = False
        for i in range(amount_rows):
            #Get category and raw_goods fields
            category = self.nocat_list.item(i,2).text()
            raw_goods = self.nocat_list.item(i,3).text()
            id = self.nocat_list.item(i,0).text()
            #Check if they are changed
            if category != '' or raw_goods != '':
                is_changes = True
                system_id = self.nocat_list.item(i,4).text()
                #Update export Data
                for val in self.nocat_indexes[system_id]:
                    row = self.imported_lines[val] 
                    row[CATEGORY_INDEX] = category
                    row[RAW_GOODS_INDEX] = raw_goods
                parser = self.get_parser_from_system_id(system_id)
                if category != '':
                    parser.update_category(id,category)
                if raw_goods != '':
                    parser.update_raw_goods(id,raw_goods)
        return is_changes

                
                #Update parser dictionary values
                    
    def update_category_file(self):
        all_category_sheets = dict()
        for (name,parser) in self.parsers.items():
            all_category_sheets[name] = parser.get_data_categories()
        write_sheets_to_excel_file(CATEGORY_FILE_PATH,all_category_sheets)

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
                #Line is an array of arrays, where each sub array is an item. a line is the same item id however
                for i in range(len(line)):
                    #the fields we need from the parsed line to add to the table, set in constants instead
                    id = str(line[i][-1])
                    name = line[i][NAME_INDEX]
                    category = line[i][CATEGORY_INDEX]
                    raw_goods = line[i][RAW_GOODS_INDEX]
                    #id for internal use, as we can get ids with same name from different parsers
                    system_id = parser.__str__() + '_' + id
                    index = self.curadded + i

                    #If we already added an entry for an ID we dont create a new row but just add it to the index list
                    if system_id in self.nocat_indexes:
                        self.nocat_indexes[system_id].append(index)
                    else:
                        #Add the missing item as a row in the no categories table
                        add_to_table(self.nocat_list,id,name,category,raw_goods,system_id)
                        #Add ID to the index list so we know which line was added in the no category table
                        self.nocat_indexes[system_id] = [index]
            return line
        except ValueError:
            return 
        except IndexError:
            return 

    def load_file(self,parsers,filepath,sheet):
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
        for (_,parser) in parsers.items():
            try:
                length = parser.load_data(filepath,sheet)
                return (length,parser)
            except ParserError:
                pass
            except InvalidFileFormatError:
                pass
            except KeyError:
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

    def get_parser_from_system_id(self,system_id):
        parser_name = system_id.split('_')[0]
        return self.parsers[parser_name]