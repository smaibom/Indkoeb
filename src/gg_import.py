import pandas as pd
from constants import GG_HEADERS
from import_class import Import_Class
from import_files import import_csv


class GG_Import(Import_Class):

    def get_price_per_unit(self,line):
        index = self.static_vals['price_per_unit_index']
        #Value is xx,xx kr string. We take the first 5 chars and change the , to a . for float conversion
        val = line[index][:5]
        val = val.replace(',','.')
        return float(val)

    def get_total_price(self,line):
        index = self.static_vals['total_price_index']
        #Format is using thousand seperate with . and decimal seperator as , with "kr" in the end
        value = line[index][:-4]
        #Remove thousand seperators
        value = value.replace('.','')
        #Change the decimal seperator to . to allow conversion to float
        value = value.replace(',','.')
        return float(value)

    def get_total_kg(self,line):
        index = self.static_vals['total_weight_index']
        #Its just an integer in string format
        value = int(line[index])
        #Value is in grams, divide by 1000 for kgs
        return value/1000

    def get_type(self,string):
        if string == '1':
            return 'Øko'
        return 'Konv'

    def import_data(self,csv):
        df_data = import_csv(csv,GG_HEADERS)
        rows = []
        year = self.get_year()
        quarter = self.get_quarter()
        source = self.get_source()
        for i in range(len(df_data)):
            line = df_data.loc[i]
            try:
                #Empty line
                if pd.isna(line[0]):
                    continue
                #Header, skip to next entry
                elif line[0] == 'Source No_':
                    continue
                #If the entry on first column is not a number and the other checks have passed its the hospital name
                elif not line[0].isnumeric():
                    hospital = self.get_hospital(line[0],False)
                #No checks were met, so its a numeric entry that denotes an item line
                id = int(line[0])
                category = self.get_category(id)
                raw_goods = self.get_raw_goods(id)

                #Type is in 9th column
                conv_or_eco = self.get_type(line[8])

                #Name is on 3rd column
                variant = " ".join(line[2].split())
                price_per_unit = self.get_price_per_unit(line)
                total_price = self.get_total_price(line)
                amount_kg = self.get_total_kg(line)
                price_per_kg = total_price/amount_kg
                origin_country = 'DK'
                newrow = [year,quarter,hospital,category,source,raw_goods,conv_or_eco,
                    variant,price_per_unit,total_price,amount_kg,price_per_kg,origin_country,None,None,None,None,None,None,None,None]
                rows.append(newrow)

            except ValueError:
                #print(e)
                pass
        return rows


