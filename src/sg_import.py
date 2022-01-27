from os import listdir
import pandas as pd
from constants import COLUMN_NAMES, HK, SG, SG_HOSPITALS
from import_class import Import_Class
from import_files import export_excel, import_excel


class sg_import(Import_Class):
    def get_hospital(self,name):
        #The short name is in a bracket in the string
        short_name = name.split(')')[0].split('(')[1]
        return SG_HOSPITALS[short_name]

    def strip_sg_item_name(self,name):
        if 'øko' in name.lower():
            name = ''.join(name.split('-')[:-1])
            return name.rstrip()
        return name

    
    def translate_sg_data(self,filename,df_sg_id_data):
        df_hospital_data = import_excel(filename)
        year = self.get_year()
        quarter = self.get_quarter()
        source = self.get_source()
        #The hospital info is on the 2nd row of the sheet
        hospital = self.get_hospital(df_hospital_data.iloc[1,0])
        #Data starts from row 5-6 in the excel sheet
        rows = []
        for i in range(4,len(df_hospital_data)):
            line = df_hospital_data.iloc[i]
            #We ignore the line where they total up
            if pd.isna(line[0]):
                continue
            elif 'Total' in line[0]:
                continue
            #New grouping line
            elif line[0] == 'Gruppe':
                continue
            #Empty line
            id = line[1]
            item_info = self.get_item_row_from_id(df_sg_id_data,id)

            category = self.get_category(item_info)
            raw_goods = self.get_raw_goods(item_info)


            conv_or_eco = self.get_type(line[0])
            
            variant = self.strip_sg_item_name(line[2])
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

def translate_sg_dir(dir):
    files = listdir(dir)
    arr = []
    ids = 'C:\\Users\\KOM\\Documents\\Indkoeb\\StatiskData\\sg-id-type.xlsx'
    df_sg_id_data = import_excel(ids)
    sg = sg_import(SG)
    for filename in files:
        #The temp file created by excel when file is opened
        if '~$' in filename:
            continue
        filename = dir + '\\' + filename
        res = sg.translate_sg_data(filename,df_sg_id_data)
        arr = arr + res
    res = pd.DataFrame(arr,columns = COLUMN_NAMES)
    export_excel(res,'test.xlsx')
dir = 'Specialisterne\\Frisksnit'
translate_sg_dir(dir)
            