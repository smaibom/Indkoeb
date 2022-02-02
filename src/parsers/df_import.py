
import pandas as pd
from src.constants import DF
from src.errors import InvalidFileFormatError, NoCategoryError, ParserError
from src.parsers.import_class import Import_Class
from src.excel_file_functions import import_excel, import_excel_sheet
import re


class DF_Import(Import_Class):
    def __init__(self):
        super().__init__(DF)
    
    def __str__(self):
        return 'df'

    def get_hospitals_from_line(self,line):
        #the 5th column is where the first hospital data will occur
        for i in range(4,len(line),4):
            if not pd.isna(line[i]):
                hospital_id = line[i].split(' ')[0]
                hospital = self.get_hospital(int(hospital_id))
                self.hospitals.append(hospital)


    def load_data(self,filename,sheet):
        try:
            self.data = import_excel_sheet(filename,sheet,self.static_vals['file_start'])
            #Hospital data is in row 7 so we start from there, headers is afterwards

            self.check_headers(self.data.loc[1])

            self.hospitals = ['']

            #Hospital data is in the first line we import
            self.get_hospitals_from_line(self.data.loc[0])
            #Skip past headers + hospital
            self.data = self.data.loc[2:].reset_index()

            #DF data dosent have any indicators for what to ignore so we have a ignore file with data
            self.ignore = import_excel('StatiskData\\df_ignore.xlsx',import_header = True)
            return len(self.data)
        except ValueError:
            raise InvalidFileFormatError()
        except AttributeError:
            raise ParserError()

    def parse_line(self,index,allow_nocat = False):
        line = self.data.loc[index]
        #Check if first value is a number, all entries are numbers in DF
        try:
            if not line[0].isnumeric():
                return
        except AttributeError:
            return
        year = self.get_year()
        quarter = self.get_quarter()
        source = self.get_source()
        conv_or_eco = self.get_type(line[2])
        origin_country = line[3]
        item_id = line[0]
        if self.is_ignored(self.ignore,item_id):
            return
        item_id = int(item_id)
        category = self.get_category(item_id)
        raw_goods = self.get_raw_goods(item_id)
        if not category:
            if allow_nocat:
                category = ''
            else:
                raise NoCategoryError
        if not raw_goods:
            if allow_nocat:
                raw_goods = ''
            else:
                raise NoCategoryError
        #For some reason pandas report the length of the line as larger than it is when using length
        length = line.index[-1]+1
        rows = []
        for j in range(4,length,4):
            try:
                if not pd.isna(line[j]):
                    hospital = self.hospitals[j//4]
                    variant = self.sanitize_name(line[1])
                    amount_kg = self.get_total_kg(line,j+1)
                    total_price = self.get_total_price(line,j+2)
                    price_per_unit = line[j+3]
                    price_per_kg = total_price/amount_kg
                    row = [year,quarter,hospital,category,source,raw_goods,conv_or_eco,
                                variant,price_per_unit,total_price,amount_kg,price_per_kg,origin_country,None,None,None,None,None,None,None,None,item_id]
                    rows.append(row)
            except ValueError:
                pass
        return rows

    def get_type(self,string):
        if string.lower() == 'nej':
            return 'Konv'
        elif string.lower() == 'ja':
            return 'Øko'
        return '-'

    def sanitize_name(self,name):
        name = re.compile(re.escape('#')).sub('',name)
        name = re.compile(re.escape('øko'),re.IGNORECASE).sub('',name)
        return " ".join(name.split())
    
    def is_ignored(self,df,id):
        row = df.loc[df['ID'] == int(id)]
        if row.empty:
            return False
        return True

    def get_total_price(self,line,index):
        val = float(line[index])
        if val == 0:
            raise ValueError()
        return val
    
    def get_total_kg(self,line,index):
        val = float(line[index])
        if val == 0:
            raise ValueError()
        return val
    
"""
    def import_data(self,filename):
        ignore = import_excel('StatiskData\\df_ignore.xlsx')
        df_data = import_excel(filename)
        year = self.get_year()
        quarter = self.get_quarter()
        source = self.get_source()
        rows = []
        for i in range(len(df_data)):
            line = df_data.loc[i]
            if pd.isna(line[0]):
                continue
            #Hospitals are 1 line above the start of the list
            elif line[0] == 'Varenr.':
                hospital_line = df_data.loc[i-1]
                continue
            #End of the items
            elif line[0] == 'Summary':
                return rows 
            #Data starts from column 5
            conv_or_eco = self.get_type(line[2])
            origin_country = line[3]
            item_id = line[0]
            if self.is_ignored(ignore,item_id):
                continue
            item_id = int(item_id)
            try:
                category = self.get_category(item_id)
                raw_goods = self.get_raw_goods(item_id)
            except NoCategoryError:
                category = ""
                raw_goods = ""
            for j in range(4,len(line),4):
                try:
                    if not pd.isna(line[j]):
                        hospital_id = hospital_line[j].split(' ')[0]
                        hospital = self.get_hospital(int(hospital_id))

                        variant = self.sanitize_name(line[1])
                        amount_kg = self.get_total_kg(line,j+1)
                        total_price = self.get_total_price(line,j+2)
                        price_per_unit = line[j+3]
                        price_per_kg = total_price/amount_kg
                        row = [year,quarter,hospital,category,source,raw_goods,conv_or_eco,
                                    variant,price_per_unit,total_price,amount_kg,price_per_kg,origin_country,None,None,None,None,None,None,None,None]
                        rows.append(row)
                except ValueError:
                    pass
        return rows

    def import_dir(self,dir):
        files = listdir(dir)
        arr = []
        for filename in files:
            #The temp file created by excel when file is opened
            if '~$' in filename:
                continue
            filepath = dir + '\\' + filename
            res = self.import_data(filepath)
            arr = arr + res
        return arr
"""
