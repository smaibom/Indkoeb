
from os import listdir
import pandas as pd
from import_class import Import_Class
from import_files import import_excel
from constants import DF
from constants import COLUMN_NAMES
import re
from import_files import export_excel


class DF_Import(Import_Class):
    def get_type(self,string):
        if string.lower() == 'nej':
            return 'Konv'
        elif string.lower() == 'ja':
            return 'Øko'
        return '-'

    def sanitize_name(self,name):
        name = re.compile(re.escape('#')).sub('',name)
        name = re.compile(re.escape('øko'),re.IGNORECASE).sub('',name)
        return name.strip()
    
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
            category = self.get_category(item_id)
            raw_goods = self.get_raw_goods(item_id)
            for j in range(4,len(line),4):
                try:
                    if not pd.isna(line[j]):
                        hospital_id = hospital_line[j].split(' ')[0]
                        hospital = self.get_hospital(hospital_id,True)

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

path = 'Specialisterne\\Dagrofa'

df = DF_Import(DF)
data = df.import_dir(path)
res = pd.DataFrame(data,columns = COLUMN_NAMES)
export_excel(res,'test.xlsx')