
import pandas as pd
from src.constants import EM
from src.errors import InvalidFileFormatError, NoCategoryError, ParserError
from src.parsers.import_class import Import_Class
from src.excel_file_functions import import_excel_sheet


class EM_Import(Import_Class):
    def __init__(self):
        super().__init__(EM)

    def __str__(self):
        return 'em'

    def load_data(self,filename,sheet):
        try:
            self.data = import_excel_sheet(filename,sheet)
            self.check_headers(self.data.loc[0])
            self.hospital = self.get_hospital(sheet)
            #Skip past total data
            self.data = self.data.loc[4:].reset_index()
            return len(self.data)
        except ValueError:
            raise InvalidFileFormatError()
        except AttributeError:
            raise ParserError()

    def parse_line(self,index,allow_nocat = False):
        line = self.data.loc[index]

        if pd.isna(line[0]) or line[0] == 'Produktnavn':
            return

        year = self.get_year()
        quarter = self.get_quarter()
        source = self.get_source()
        conv_or_eco = self.get_type(line[1])
        variant = " ".join(self.get_variant(line[0]).split())
        category = self.get_category(variant)
        raw_goods = self.get_raw_goods(variant)
        if not category:
            if allow_nocat:
                category = ''
            else:
                raise NoCategoryError
        if not raw_goods:
            if allow_nocat:
                raw_goods = ''
            else:
                raise NoCategoryError
        price_per_unit = self.get_price_per_unit(line)
        total_price = self.get_total_price(line)
        amount_kg = self.get_total_kg(line)
        price_per_kg = total_price/amount_kg
        origin_country = ''
        row = [year,quarter,self.hospital,category,source,raw_goods,conv_or_eco,
                variant,price_per_unit,total_price,amount_kg,price_per_kg,origin_country,None,None,None,None,None,None,None,None,variant]
        return [row]


    def get_variant(self,name):
        if 'øko' in name.lower():
            return name.rstrip()[:-4]
        return name



"""
    def import_data(self,filename):
        rows = []
        year = self.get_year()
        quarter = self.get_quarter()
        source = self.get_source()
        

        sheets = get_excel_sheet_names(filename)
        for sheet in sheets:
            try:
                hospital = self.get_hospital(sheet,False)
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
                variant = " ".join(self.get_variant(line[0]).split())
                try:
                    category = self.get_category(variant)
                    raw_goods = self.get_raw_goods(variant)
                except NoCategoryError:
                    category = ""
                    raw_goods = ""
                price_per_unit = self.get_price_per_unit(line)
                total_price = self.get_total_price(line)
                amount_kg = self.get_total_kg(line)
                price_per_kg = total_price/amount_kg
                origin_country = ''
                row = [year,quarter,hospital,category,source,raw_goods,conv_or_eco,
                        variant,price_per_unit,total_price,amount_kg,price_per_kg,origin_country,None,None,None,None,None,None,None,None]
                rows.append(row)
        return rows
    """
