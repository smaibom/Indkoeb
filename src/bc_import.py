import pandas as pd
from import_class import Import_Class
from import_files import  import_excel
import re

class BC_Import(Import_Class):

    def is_hospital(self,name):
        regex = r'\d+-\d+.+'
        res = re.match(regex,name)
        if res:
            return True
        return False

    def get_total_kg(self,line,type):
        if type == 'Konv':
            return line[self.static_vals['total_weight_konv_index']]
        elif type == 'Øko':
            return line[self.static_vals['total_weight_eco_index']]
        else:
            return line[self.static_vals['total_weight_unknown_index']]

    def is_section(self,string):
        regex = r'\d+ .+'
        res = re.match(regex,string)
        if res:
            return True
        return False

    def get_type(self,line):
        if not pd.isna(line[8]):
            return 'Øko'
        elif not pd.isna(line[9]):
            return 'Konv'
        elif not pd.isna(line[10]):
            return '-'

    def import_data(self,filename):
        df_bc_data = import_excel(filename)

        rows = []
        year = self.get_year()
        quarter = self.get_quarter()
        source = self.get_source()
        section_pass = False
        hospital = ""

        for i in range(3,len(df_bc_data)):
            try:
                line = df_bc_data.iloc[i]
                #Empty lines contains no data
                if pd.isna(line[0]):
                    if not pd.isna(line[1]):
                        if self.is_hospital(line[1]):
                            #Some hospitals got # in their string that dosent exist in the data
                            hospital_name = line[1].replace('#','')
                            try:
                                hospital = self.get_hospital(hospital_name,False)
                            except KeyError:
                                hospital = 'no_id'
                            pass
                        elif self.is_section(line[1]):
                            #sections are defined by XX - <section name>, xx is the 2 numbers. Anything in 9x section is not related to food services
                            #89 is also a non food service number
                                numbers = line[1][:2]
                                if '9' == line[1][0] or '89' == numbers:
                                    section_pass = True
                                else:
                                    section_pass = False
                    continue
                if section_pass:
                    continue
                name = line[1]
                conv_or_eco = self.get_type(line)
                variant = " ".join(name.split())
                id = line[0]
                category = self.get_category(id)
                raw_goods = self.get_raw_goods(id)
                price_per_unit = self.get_price_per_unit(line)
                total_price = self.get_total_price(line)
                amount_kg = self.get_total_kg(line,conv_or_eco)
                price_per_kg = total_price/amount_kg
                origin_country = line[16]
                row = [year,quarter,hospital,category,source,raw_goods,conv_or_eco,
                    variant,price_per_unit,total_price,amount_kg,price_per_kg,origin_country,None,None,None,None,None,None,None,None]
                rows.append(row)
            except ValueError:
                pass
        return rows
