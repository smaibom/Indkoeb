
import pandas as pd
from import_class import Import_Class
from import_files import get_excel_sheet_names, import_excel_sheet,export_excel
from constants import EM,COLUMN_NAMES


class EM_Import(Import_Class):

    def get_variant(self,name):
        if 'øko' in name.lower():
            return name.rstrip()[:-4]
        return name


    def import_data(self,filename):
        rows = []
        year = self.get_year()
        quarter = self.get_quarter()
        source = self.get_source()
        

        sheets = get_excel_sheet_names(filename)
        for sheet in sheets:
            try:
                hospital = self.get_hospital(sheet)
            except KeyError:
                #The hospital dosent exist in file
                continue
            df_data = import_excel_sheet(filename,sheet)

            #Skip headers in files
            for i in range(3,len(df_data)):
                line = df_data.loc[i]

                #First column with no content or "produktnavn" is skipable
                if pd.isna(line[0]) or line[0] == 'Produktnavn':
                    continue

                conv_or_eco = self.get_type(line[1])
                variant = self.get_variant(line[0])
                category = self.get_category(variant)
                raw_goods = self.get_raw_goods(variant)
                price_per_unit = self.get_price_per_unit(line)
                total_price = self.get_total_price(line)
                amount_kg = self.get_total_kg(line)
                price_per_kg = total_price/amount_kg
                origin_country = ''
                row = [year,quarter,hospital,category,source,raw_goods,conv_or_eco,
                        variant,price_per_unit,total_price,amount_kg,price_per_kg,origin_country,None,None,None,None,None,None,None,None]
                rows.append(row)
        return rows

em = EM_Import(EM)
fp = 'Specialisterne\\Emmerys 01-04-2021..30-06-2021.xlsx'

data = em.import_data(fp)
res = pd.DataFrame(data,columns = COLUMN_NAMES)
#export_excel(res,'test.xlsx')