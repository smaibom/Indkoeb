from constants import AC, AC_CLIENT_HOSPITAL_HEADERS, COLUMN_NAMES
import re
from os import listdir
import pandas as pd
from import_class import Import_Class
from import_files import export_excel, import_excel

class Ac_Import(Import_Class):
    def get_hospital_nr_from_filename(self,filename):
        """
        Splits a AC filename and takes the client number 
        A file in the AC folder follows the format of '<clientnumber> <hospital information>' The end part of the hopsital information 
        is not consistant but the client number is always first seperated by a space so we only use that information
        """
        #Its always the first element of the filename
        number = filename.split(' ')[0]
        return number

    def get_variant(self,name):
        """
        Names in files are listed as "ØKO item (country)" ØKO is optional
        """
        name = name.rstrip()
        if 'ØKO' in name:
            name = name[4:]
        name = name.split('(')[0]
        return " ".join(name.split())

    def get_origin_country(self,name):
        if '(0)' in name:
            raise ValueError('Not valid country')
        try:
            name = name.rstrip().split('(')[1].split(')')[0]
        except:
            return ""
        if len(name) <2 or len(name) > 5:
            return ""
        return name



    def get_data_from_ac_file(self,dir,filename):
        df = import_excel(dir + '\\' + filename)

        year = self.get_year()
        quarter = self.get_quarter()

        client_nr = self.get_hospital_nr_from_filename(filename)
        try:
            hospital = self.get_hospital(client_nr,True)
        except KeyError:
            return []
        source = self.get_source()
        rows = []
        for i in range(len(df)):
            try:
                line = df.iloc[i]
                name = df.iloc[i,3]
                conv_or_eco = self.get_type(name)
                variant = self.get_variant(name)
                price_per_unit = self.get_price_per_unit(line)
                total_price = self.get_total_price(line)

                id = df.iloc[i,2]
                category = self.get_category(id)
                raw_goods = self.get_raw_goods(id)
                #Validation check
                self.get_unit_amount(line)
                amount_kg = self.get_total_kg(line)
                price_per_kg = total_price/amount_kg
                origin_country = self.get_origin_country(name)
                rows.append([year,quarter,hospital,category,source,raw_goods,conv_or_eco,
                            variant,price_per_unit,total_price,amount_kg,price_per_kg,origin_country,None,None,None,None,None,None,None,None])
            except ValueError:
                pass

        return rows



def import_all_files_ac(dir):
    files = listdir(dir)
    arr = []
    ac = Ac_Import(AC)
    for filename in files:
        #The temp file created by excel when file is opened
        if '~$' in filename:
            continue
        res = ac.get_data_from_ac_file(dir,filename)
        arr = arr + res
    res = pd.DataFrame(arr,columns = COLUMN_NAMES)
    export_excel(res,'test.xlsx')
p = 'C:\\Users\\KOM\\Documents\\Indkoeb\\Specialisterne\\AC\\Ny mappe'
import_all_files_ac(p)
#import_all_files_ac(p)