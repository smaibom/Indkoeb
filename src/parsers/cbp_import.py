
from src.errors import InvalidFileFormatError, ParserError
from src.import_files import import_excel_sheet
from src.parsers.import_class import Import_Class
import re

from src.constants import CBP


class CBP_Import(Import_Class):
    def __init__(self):
        super().__init__(CBP)
    
    def load_data(self,filename):
        try:
            self.data = import_excel_sheet(filename,'Sheet1')
            self.hospital = "no_id"
            return len(self.data)
        except ValueError:
            raise InvalidFileFormatError()
        except AttributeError:
            raise ParserError()

    def get_type(self,string):
        if string == 'Ej Økologi':
            return 'Konv'
        elif string == 'Økologi':
            return 'Øko'
        return '-'
    
    def get_name(self,name):
        #Taking a string with digits first and a optional øko and returning whats left after those things
        prog = re.compile('\d+ ~(?: Øko)?(.+)') 
        name = prog.match(name).group(1)
        return name

    def import_data(self,filename):
        df_data = import_excel_sheet(filename,'Sheet1')
        year = self.get_year()
        quarter = self.get_quarter()
        source = self.get_source()
        hospital = 'no_id'
        rows = []
        for i in range(len(df_data)):
            line = df_data.loc[i]
            category = ''
            raw_goods = ''
            conv_or_eco = self.get_type(line[10])
            variant = " ".join(self.get_name(line[1]).split())

            #No amount of units and no price per unit, so cant calculate
            price_per_unit = ''
            try:
                total_price = self.get_total_price(line)
                amount_kg = self.get_total_kg(line)
            except ValueError:
                continue
            price_per_kg = total_price/amount_kg
            origin_country = ''
            row = [year,quarter,hospital,category,source,raw_goods,conv_or_eco,
                variant,price_per_unit,total_price,amount_kg,price_per_kg,origin_country,None,None,None,None,None,None,None,None]
            rows.append(row)
        return rows

