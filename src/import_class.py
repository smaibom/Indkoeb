from constants import HOSPITALS_TRANSLATE_FILE_PATH,CATEGORY_FILE_PATH
from import_files import import_excel_sheet


class Import_Class:
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
        return self.static_vals['year'] 

    def get_quarter(self):
        return self.static_vals['quarter']

    def get_source(self):
        return self.static_vals['source']

    def get_total_price(self,line):
        index = self.static_vals['total_price_index']
        return float(line[index])

    def get_category(self,id):
        row = self.df_data_categories.loc[self.df_data_categories['ID'] == id]
        if row.empty:
            return ""
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
        string = string.lower()
        if 'øko' in string:
            return 'Øko'
        return 'Konv'       

    def get_total_kg(self,line):
        index = self.static_vals['total_weight_index']
        val = float(line[index])
        if val == 0:
            raise ValueError()
        return val
    
    def get_unit_amount(self,line):
        index = self.static_vals['units_index']
        val = float(line[index])
        if val == 0:
            raise ValueError()
        return val

    def get_price_per_unit(self,line):
        index = self.static_vals['price_per_unit_index']
        val = float(line[index])
        return val
    
    def get_total_price(self,line):
        index = self.static_vals['total_price_index']
        val = float(line[index])
        if val == 0:
            raise ValueError()
        return val
