from multiprocessing import Value
import pandas as pd
from src.constants import HOSPITALS_TRANSLATE_FILE_PATH,CATEGORY_FILE_PATH
from src.import_files import import_excel_sheet
from src.errors import NoCategoryError


class Import_Class:
    """
    The superclass for import files
    """
    def __init__(self,static_vals):
        self.static_vals = static_vals
        id = static_vals['source'].lower()
        self.df_hospital_vals = import_excel_sheet(HOSPITALS_TRANSLATE_FILE_PATH,id)
        self.df_data_categories = import_excel_sheet(CATEGORY_FILE_PATH,id)

    def get_hospital(self,string,is_number):
        if is_number:
            string = int(string)
        hospital = self.df_hospital_vals.loc[self.df_hospital_vals['Original'] == string]
        if hospital.empty:
            raise KeyError
        return hospital.iloc[0,1]

    def get_year(self):
        """
        Gets the static value year of the object
        returns:
            The int value for the value year
        """
        return self.static_vals['year'] 

    def get_quarter(self):
        """
        Gets the static value quarter of the object
        returns:
            The string value of the quarter
        """
        return self.static_vals['quarter']

    def get_source(self):
        """
        Gets the static value source of the object
        returns:
            The string value of the source
        """
        return self.static_vals['source']

    def get_total_price(self,line):
        index = self.static_vals['total_price_index']
        return float(line[index])

    def get_category(self,id):
        row = self.df_data_categories.loc[self.df_data_categories['ID'] == id]
        if row.empty:
            raise NoCategoryError()
        #Categories is in the 2nd column
        category = row.iloc[0,1]
        return category

    def get_raw_goods(self,id):
        row = self.df_data_categories.loc[self.df_data_categories['ID'] == id]
        if row.empty:
            return ""
        # is in column 3
        raw_goods = row.iloc[0,2]
        return raw_goods

    def get_type(self,string):
        """
        """
        string = string.lower()
        if 'øko' in string:
            return 'Øko'
        return 'Konv'       

    def get_total_kg(self,line):
        """
        Returns the total weight of an item in kg, a static value must be assigned in the constants file for the index for this to work
        returns:
            float value of the total kg
        throws:
            ValueError is value is 0
        """
        index = self.static_vals['total_weight_index']
        val = float(line[index])
        if val == 0:
            raise ValueError()
        return val
    
    def get_unit_amount(self,line):
        """
        Returns the unit amount of an item, a static value must be assigned in the constants file for the index for this to work
        returns:
            float value of the unit amount
        throws:
            ValueError is value is 0
        """
        index = self.static_vals['units_index']
        val = float(line[index])
        if val == 0:
            raise ValueError()
        return val

    def get_price_per_unit(self,line):
        """
        Returns the price per unit of a item, a static value must be assigned in the constants file for the index
        returns:
            float value of the price per unit
        """
        index = self.static_vals['price_per_unit_index']
        val = float(line[index])
        return val
    
    def get_total_price(self,line):
        """
        Returns the total price of a item, a static value must be assigned in the constants file for the index
        returns:
            float value of the total price
        throws:
            ValueError is value is 0
        """
        index = self.static_vals['total_price_index']
        val = float(line[index])
        if val == 0:
            raise ValueError()
        return val

    def check_headers(self,line):
        """
        Function that checks if a given array of string values is equal in values to a set of string values
        args:
            line: String array
        throws:
            ValueError: If the line array do not match the static array
        """
        for i in range(len(self.static_vals['headers'])):
            val_header = self.static_vals['headers'][i]
            val_line = line[i]
            if pd.isna(val_line):
                val_line = ''
            if  val_line != val_header:
                raise ValueError()
