import pandas as pd
from src.constants import CATEGORY_FILE_HEADERS, HOSPITALS_TRANSLATE_FILE_PATH,CATEGORY_FILE_PATH
from src.excel_file_functions import import_excel_sheet
from src.errors import NoCategoryError


class Import_Class:
    """
    The superclass for import files
    """
    def __init__(self,static_vals):
        """
        Constructor for Import_Class, designed to be inherieted to use some functions that are generic for each parser.
        a sheet with the name of source is required in the hospitals translate file and categories file
        args:
            static_vals: A dictionary with static values for the import class.
                         Dictionary fields: '
                            'year' : int of the year the data is parsed as, 
                            'source' : string of the source of the file the parser, 
                            'quarter' : string quarter of the year,
                            'total_price_index' : int index in the excel file for total price, 
                            'total_weight_index' : int index in the excel file for the total weight,
                            'price_per_unit_index' : int index in the excel file for the price per unit 
                            'units_index' : int index in the excel file for the amount of units

        """
        self.static_vals = static_vals
        id = static_vals['source'].lower()
        self.df_hospital_vals = import_excel_sheet(HOSPITALS_TRANSLATE_FILE_PATH,id,import_header=True)
        self.df_data_categories = import_excel_sheet(CATEGORY_FILE_PATH,id,import_header=True)

    def __str__(self):
        return self.__class__.__name__

    def get_data_categories(self):
        """
        Gets the dataframe for the category/rawgoods data for the assosiated parser
        returns:
            DataFrame with Category/Raw_goods 
        """
        return self.df_data_categories

    def update_category(self,id,category):
        """
        Updates or adds an ID for categories in the category file
        args:
            id: Value of the id of the item being searched for
            category: Value to be inserted
        """
        if id.isnumeric():
            id = int(id)
        row = self.df_data_categories.loc[self.df_data_categories['ID'] == id]
        if row.empty:
            row = pd.DataFrame([[id,category,None]],columns = CATEGORY_FILE_HEADERS)
            self.df_data_categories = pd.concat([self.df_data_categories,row],ignore_index=True)
        else:
            index = row.index.tolist()[0]
            self.df_data_categories.iloc[index,1] = category

    def update_raw_goods(self,id,raw_goods):
        """
        Updates or adds an ID for raw goods in the category file
        args:
            id: Value of the id of the item being searched for
            raw_goods: Value to be inserted
        """
        if id.isnumeric():
            id = int(id)
        row = self.df_data_categories.loc[self.df_data_categories['ID'] == id]
        if row.empty:
            row = pd.DataFrame([[id,None,raw_goods]],columns = CATEGORY_FILE_HEADERS)
            self.df_data_categories = pd.concat([self.df_data_categories,row],ignore_index=True)
        else:
            index = row.index.tolist()[0]
            self.df_data_categories.iloc[index,2] = raw_goods

    def get_hospital(self,id):
        """
        Function for getting the hospital name from the static hospital file. If the ID is a int in the excel file 
        cast the id to an int before passing to this function
        args:
            id: Value to match in the hospital file, cast to the datatype matching in the excel sheet
        returns:
            string value with the hospital category
        throws:
            KeyError: If the id does nto exist in file
        """
        hospital = self.df_hospital_vals.loc[self.df_hospital_vals['Original'] == id]
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
        """
        Gets the total_price price from a line, if this function is used 'total_price_index' must have been assigned in the static values passed in the constructor of the object
        args:
            line: A array of the values of a line in an excel sheet
        returns:
            The float value of the total price
        """
        index = self.static_vals['total_price_index']
        return float(line[index])

    def get_category(self,id):
        """
        Gets the category from the static value files for categories
        args:
            id: Value of the ID matching in the categories excel sheet, must assign the type of id to match the type in the excel sheet
        returns:
            string value of the category
            None if no id matches or the entry is empty
        """
        row = self.df_data_categories.loc[self.df_data_categories['ID'] == id]
        if row.empty:
            return None
        #Categories is in the 2nd column
        category = row.iloc[0,1]
        if pd.isna(category):
            return None
        return category

    def get_raw_goods(self,id):
        """
        Gets the raw goods from the static value files for categories, it is the sub category for a category
        args:
            id: Value of the ID matching in the categories excel sheet, must assign the type of id to match the type in the excel sheet
        returns:
            string value of the raw goods
            None if no id matches or the entry is empty
        """
        row = self.df_data_categories.loc[self.df_data_categories['ID'] == id]
        if row.empty:
            return None
        # is in column 3
        raw_goods = row.iloc[0,2]
        if pd.isna(raw_goods):
            return None
        return raw_goods

    def get_type(self,string):
        """
        Gets the type of the line, type is if it is eco or konventional, used if 'øko' is present in the name of the item
        arg:
            string of the name of the item
        returns:
            'Øko' if øko is present in the name, else 'Konv'
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

        val = line[index]
        if pd.isna(val):
            raise ValueError()
        val = float(val)
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
        val = line[index]
        if pd.isna(val):
            raise ValueError()
        val = float(val)
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
        val = line[index]
        if pd.isna(val):
            raise ValueError()
        val = float(val)
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
        val = line[index]
        if pd.isna(val):
            raise ValueError()
        val = float(val)
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
