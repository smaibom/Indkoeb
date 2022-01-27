

from unicodedata import category

import pandas as pd
from import_class import Import_Class
from import_files import import_excel_sheet,export_excel
from constants import HK,COLUMN_NAMES


class HK_Import(Import_Class):
    
    def get_type(self,value):
        if value == 'J':
            return 'Øko'
        elif value == 'N':
            return 'Konv'


    def import_data(self,filename):
        sections_to_ignore = ['Non food, etc.','Gastronomie- & storkøkkentilbehør','Engangsmaterialer / folier / filter','Rengøring & hygiene']

        df_data = import_excel_sheet(filename,'Seite1_2')
        year = self.get_year()
        quarter = self.get_quarter()
        source = self.get_source()

        rows = []
        
        for i in range(1,len(df_data)):
            try:
                line = df_data.loc[i]
                #Error in their data? remove later
                if 'HØ                             3KG' in line[3]:
                    pass               
                elif line[4] in sections_to_ignore:
                    continue

                hospital = self.get_hospital(line[0],True)
                id = line[2]
                category = self.get_category(id)
                raw_goods = self.get_raw_goods(id)
                conv_or_eco = self.get_type(line[6])
                variant = line[3]
                total_price = self.get_total_price(line)
                units = self.get_unit_amount(line)
                price_per_unit = total_price/units
                amount_kg = self.get_total_kg(line)
                price_per_kg = total_price/amount_kg
                origin_country = line[7]
                row = [year,quarter,hospital,category,source,raw_goods,conv_or_eco,
                       variant,price_per_unit,total_price,amount_kg,price_per_kg,origin_country,line[2],None,None,None,None,None,None,None]
                rows.append(row)
            except ValueError:
                pass
        return rows


hk = HK_Import(HK)
data = hk.import_data('Specialisterne\\Hørkram.xlsx')
res = pd.DataFrame(data,columns = COLUMN_NAMES)
export_excel(res,'test.xlsx')