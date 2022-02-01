import pandas as pd
from src.constants import GG, GG_CSV_HEADERS,GG_HEADERS
from src.errors import InvalidFileFormatError, NoCategoryError, ParserError
from src.parsers.import_class import Import_Class
from src.import_files import import_csv


class GG_Import(Import_Class):
    def __init__(self):
        super().__init__(GG)

    def load_data(self,filename,sheet):
        try:
            self.data = import_csv(filename,GG_CSV_HEADERS)
            self.check_headers(self.data.loc[1])
            self.hospital = ""
            return len(self.data)
        except ValueError:
            raise InvalidFileFormatError()
        except AttributeError:
            raise ParserError()

    def parse_line(self,index,allow_nocat = False):
        line = self.data.loc[index]
        #Empty line
        if pd.isna(line[0]):
            return
        #Header, skip to next entry
        elif line[0] == 'Source No_':
            return
        #If the entry on first column is not a number and the other checks have passed its the hospital name
        elif not line[0].isnumeric():
            self.hospital = self.get_hospital(line[0],False)
            

        year = self.get_year()
        quarter = self.get_quarter()
        source = self.get_source()
        id = int(line[0])


        #Type is in 9th column
        conv_or_eco = self.get_type(line[8])

        #Name is on 3rd column
        variant = " ".join(line[2].split())
        price_per_unit = self.get_price_per_unit(line)
        total_price = self.get_total_price(line)
        amount_kg = self.get_total_kg(line)
        price_per_kg = total_price/amount_kg
        origin_country = 'DK'
        try:
            category = self.get_category(id)
            raw_goods = self.get_raw_goods(id)
        except NoCategoryError:
            if allow_nocat:
                category = ''
                raw_goods = ''
            else:
                raise NoCategoryError()
        row = [year,quarter,self.hospital,category,source,raw_goods,conv_or_eco,
            variant,price_per_unit,total_price,amount_kg,price_per_kg,origin_country,None,None,None,None,None,None,None,None,id]
        return [row]


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
                try:
                    category = self.get_category(id)
                    raw_goods = self.get_raw_goods(id)
                except NoCategoryError:
                    category = ""
                    raw_goods = ""

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


