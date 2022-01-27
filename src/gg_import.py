import pandas as pd
from constants import COLUMN_NAMES, GG, GG_HEADERS, GG_HOSPITALS
from import_class import Import_Class
from import_files import export_excel, import_csv, import_excel


class GG_Import(Import_Class):

    def get_hospital(self,name):
        return GG_HOSPITALS[name]

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

    def translate_gg_data(self,csv,id_data):
        df_csv_data = import_csv(csv,GG_HEADERS)
        df_gg_id_data = import_excel(id_data)
        rows = []
        year = self.get_year()
        quarter = self.get_quarter()
        source = self.get_source()
        for i in range(len(df_csv_data)):
            line = df_csv_data.iloc[i]
            try:
                if line[0] == 'Source No_':
                    continue
                elif line[0] in GG_HOSPITALS:
                    hospital = self.get_hospital(line[0])
                    continue
                #If there is an int on the row its a entry line, if not its a line we dont care about and its skipped in the error handler
                id = int(line[0])

                item_info = self.get_item_row_from_id(df_gg_id_data,id)

                category = self.get_category(item_info)
                raw_goods = self.get_raw_goods(item_info)
                #Name is on 3rd column
                name = line[2]
                conv_or_eco = self.get_type(name)
                variant = name
                price_per_unit = self.get_price_per_unit(line)
                total_price = self.get_total_price(line)
                amount_kg = self.get_total_kg(line)
                price_per_kg = total_price/amount_kg
                origin_country = 'DK'
                newrow = [year,quarter,hospital,category,source,raw_goods,conv_or_eco,
                    variant,price_per_unit,total_price,amount_kg,price_per_kg,origin_country,None,None,None,None,None,None,None,None]
                rows.append(newrow)

            except Exception as e:
                #print(e)
                pass
        return rows

csv = 'Specialisterne\\Grønt Grossisten.csv'
ids = 'C:\\Users\\KOM\\Documents\\Indkoeb\\StatiskData\\gg-id-type.xlsx'
gg = GG_Import(GG)
rows = gg.translate_gg_data(csv,ids)
res = pd.DataFrame(rows,columns = COLUMN_NAMES)
#export_excel(res,'test.xlsx')

