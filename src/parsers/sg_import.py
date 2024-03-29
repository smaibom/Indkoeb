from os import listdir
import re
import pandas as pd
from src.constants import SG
from src.errors import InvalidFileFormatError, NoCategoryError, ParserError
from src.parsers.import_class import Import_Class
from src.excel_file_functions import  import_excel_sheet


class SG_Import(Import_Class):
    def __init__(self):
        super().__init__(SG)

    def __str__(self):
        return 'sg'

    def load_data(self,filename,sheet):
        try:
            self.data = import_excel_sheet(filename,sheet,self.static_vals['file_start'])
            self.check_headers(self.data.loc[3])
            self.hospital = self.get_hospital(self.data.iloc[0,0])
            #Dont need headers anymore
            self.data = self.data[3:].reset_index()
            return len(self.data)
        except ValueError:
            raise InvalidFileFormatError()
        except AttributeError:
            raise ParserError()
    
    def parse_line(self,index,allow_nocat = False):
        
        year = self.get_year()
        quarter = self.get_quarter()
        source = self.get_source()

        line = self.data.loc[index]

        #Empty columns got no data
        if pd.isna(line[0]):
            return
        #Skip Header of line
        elif 'Total' in line[0]:
            return
        #Another healer skip
        elif line[0] == 'Gruppe':
            return
    
        #Item id is in 2nd column
        id = line[1]

        conv_or_eco = self.get_type(line[0])
        variant = self.strip_sg_item_name(line[2].strip())
        total_price = self.get_total_price(line)
        amount_kg = self.get_total_kg(line)
        price_per_kg = total_price/amount_kg
        amount_units = self.get_unit_amount(line)
        price_per_unit = total_price/amount_units
        #No origin country for this dataset
        origin_country = ""
        category = self.get_category(id)
        raw_goods = self.get_raw_goods(id)
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
        row = [year,quarter,self.hospital,category,source,raw_goods,conv_or_eco,
                variant,price_per_unit,total_price,amount_kg,price_per_kg,origin_country,None,None,None,None,None,None,None,None,id]
        return [row]

    def strip_sg_item_name(self,name):
        #Remove the eco part of the name
        name = re.sub(' - Økologisk', '', name)
        #remove double whitespace
        name = " ".join(name.split())
        return name

    def get_name(self,string):
        prog = re.compile('([-\w ()æÆøØåÅ]+)(?: - Økologisk)')
        try:
            name = prog.match(string.strip())
            return name.group(1)
        except AttributeError:
            return string
        

    """
    def import_data(self,filename):
        df_data = import_excel(filename)
        
        year = self.get_year()
        quarter = self.get_quarter()
        source = self.get_source()

        #The hospital info is on the 2nd row and first column of the sheet
        hospital = self.get_hospital(df_data.iloc[1,0])
        #Data starts from row 5-6 in the excel sheet
        rows = []
        for i in range(4,len(df_data)):
            line = df_data.iloc[i]

            #If first column is empty on a line skip
            if pd.isna(line[0]):
                continue
            #Skip Header of line
            elif 'Total' in line[0]:
                continue
            #Another healer skip
            elif line[0] == 'Gruppe':
                continue
            
            #Item id is in 2nd column
            id = line[1]
            try:
                category = self.get_category(id)
                raw_goods = self.get_raw_goods(id)
            except NoCategoryError:
                category = ""
                raw_goods = ""
            conv_or_eco = self.get_type(line[0])
            variant = " ".join(self.strip_sg_item_name(line[2]).split())
            total_price = self.get_total_price(line)
            amount_kg = self.get_total_kg(line)
            price_per_kg = total_price/amount_kg
            amount_units = self.get_unit_amount(line)
            price_per_unit = total_price/amount_units
            #No origin country for this dataset
            origin_country = ""
            rows.append([year,quarter,hospital,category,source,raw_goods,conv_or_eco,
                    variant,price_per_unit,total_price,amount_kg,price_per_kg,origin_country,None,None,None,None,None,None,None,None])
        return rows

    def import_dir(self,dir):
        files = listdir(dir)
        arr = []
        for filename in files:
            #The temp file created by excel when file is opened
            if '~$' in filename:
                continue
            filename = dir + '\\' + filename
            res = self.import_data(filename)
            arr = arr + res
        return arr

"""
            