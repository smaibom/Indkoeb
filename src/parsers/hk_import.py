

from src.constants import HK
from src.errors import InvalidFileFormatError, NoCategoryError, ParserError
from src.parsers.import_class import Import_Class
from src.excel_file_functions import import_excel_sheet



class HK_Import(Import_Class):
    def __init__(self):
        super().__init__(HK)


    def __str__(self):
        return 'hk'

    def load_data(self,filename,sheet):
        try:
            self.data = import_excel_sheet(filename,sheet,skiprow=1)
            print(self.data.loc[0])
            self.check_headers(self.data.loc[0])
            return len(self.data)
        except ValueError:
            raise InvalidFileFormatError()
        except AttributeError:
            raise ParserError()

    def parse_line(self,index,allow_nocat = False):
        line = self.data.loc[index]
        #Only lines with a number in the first column contanis data
        if not type(line[0]) == int:
            return

        sections_to_ignore = ['Non food, etc.','Gastronomie- & storkøkkentilbehør','Engangsmaterialer / folier / filter','Rengøring & hygiene']

        year = self.get_year()
        quarter = self.get_quarter()
        source = self.get_source()
        #Error in their data? remove later  
        if line[4] in sections_to_ignore:
            return
        hospital = self.get_hospital(int(line[0]))
        id = line[2]

        conv_or_eco = self.get_type(line[6])
        variant = " ".join(line[3].split())
        total_price = self.get_total_price(line)
        units = self.get_unit_amount(line)
        price_per_unit = total_price/units
        amount_kg = self.get_total_kg(line)
        price_per_kg = total_price/amount_kg
        origin_country = line[7]
        category = self.get_category(id)
        raw_goods = self.get_raw_goods(id)
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
        row = [year,quarter,hospital,category,source,raw_goods,conv_or_eco,
                variant,price_per_unit,total_price,amount_kg,price_per_kg,origin_country,None,None,None,None,None,None,None,None,id]
        return [row]

    def get_type(self,value):
        if value == 'J':
            return 'Øko'
        elif value == 'N':
            return 'Konv'
        return '-'

    """
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

                hospital = self.get_hospital(int(line[0]))
                id = line[2]
                try:
                    category = self.get_category(id)
                    raw_goods = self.get_raw_goods(id)
                except NoCategoryError:
                    category = ""
                    raw_goods = ""
                conv_or_eco = self.get_type(line[6])
                variant = " ".join(line[3].split())
                total_price = self.get_total_price(line)
                units = self.get_unit_amount(line)
                price_per_unit = total_price/units
                amount_kg = self.get_total_kg(line)
                price_per_kg = total_price/amount_kg
                origin_country = line[7]
                row = [year,quarter,hospital,category,source,raw_goods,conv_or_eco,
                       variant,price_per_unit,total_price,amount_kg,price_per_kg,origin_country,None,None,None,None,None,None,None,None]
                rows.append(row)
            except ValueError:
                pass
        return rows
"""

