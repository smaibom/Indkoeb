import re
from src.parsers.import_class import Import_Class
from src.import_files import import_excel
from src.constants import AC
from src.errors import InvalidFileFormatError, NoCategoryError,ParserError

class AC_Import(Import_Class):
    def __init__(self):
        super().__init__(AC)

    def get_hospital_nr_from_filename(self,filename):
        """
        Splits a AC filename and takes the client number 
        A file in the AC folder follows the format of '<clientnumber> <hospital information>' The end part of the hopsital information 
        is not consistant but the client number is always first seperated by a space so we only use that information
        """
        #Its always the first element of the filename
        prog = re.compile('(\d+) .+')
        number = prog.match(filename).group(1)
        return number

    def get_variant(self,name):
        """
        Names in files are listed as "ØKO item (country)" ØKO is optional
        """
        prog = re.compile('(?:ØKO )?([,+\.\wæÆøØåÅ /-]+).*')
        new_name = prog.match(name)
        #Removing double whitepsaces between words etc
        new_name = new_name
        return " ".join(new_name.group(1).split())

    def get_origin_country(self,name):
        #Ignore everything to a ( match letts afterwards, in case a ( dosent exist it dosent have a country
        prog = re.compile('[,+\.\wæÆøØåÅ /-]+[\(](?: \()?([\w]+)?.*')
        country = prog.match(name)
        if not country:
            return ''
        country = country.group(1)
        #(0) is for items that we dont want
        if country == '0':
            raise ValueError()
        #Some countries have to few letters to decipher where its from due to misslabling
        if len(country) < 2:
            return ''
            
        return country


    def load_data(self,filename):
        try:
            self.data = import_excel(filename)
            self.check_headers(self.data.loc[0])
            hospital_nr = self.get_hospital_nr_from_filename(filename.split('/')[-1])
            self.hospital = self.get_hospital(hospital_nr,True)
            #Dont need headers anymore
            self.data = self.data.loc[1:].reset_index()
            return len(self.data)
        except ValueError:
            raise InvalidFileFormatError()
        except AttributeError:
            raise ParserError()

    def parse_line(self,index,allow_nocat = False):
        line = self.data.loc[index]
        year = self.get_year()
        quarter = self.get_quarter()
        source = self.get_source()
        hospital = self.hospital
        #Name is in the 4th column
        name = line[3]
        conv_or_eco = self.get_type(name)
        variant = self.get_variant(name)
        price_per_unit = self.get_price_per_unit(line)
        total_price = self.get_total_price(line)

        #Validation check
        self.get_unit_amount(line)
        amount_kg = self.get_total_kg(line)
        price_per_kg = total_price/amount_kg
        origin_country = self.get_origin_country(name)
        
        #Name is in the 3rd column
        id = line[2]
        try:
            category = self.get_category(id)
            raw_goods = self.get_raw_goods(id)
        except NoCategoryError:
            if allow_nocat:
                category = ''
                raw_goods = ''
            else:
                raise NoCategoryError
        row = [year,quarter,hospital,category,source,raw_goods,conv_or_eco,
                    variant,price_per_unit,total_price,amount_kg,price_per_kg,origin_country,None,None,None,None,None,None,None,None,id]
        return [row]


"""
    def import_data(self,dir,filename):
        df_data = import_excel(dir + '\\' + filename)

        year = self.get_year()
        quarter = self.get_quarter()

        client_nr = self.get_hospital_nr_from_filename(filename)
        hospital = self.get_hospital(client_nr,True)
        source = self.get_source()
        rows = []
        for i in range(len(df_data)):
            try:
                line = df_data.loc[i]
                #Name is in the 4th column
                name = line[3]
                conv_or_eco = self.get_type(name)
                variant = self.get_variant(name)
                price_per_unit = self.get_price_per_unit(line)
                total_price = self.get_total_price(line)

                #Name is in the 3rd column
                id = line[2]

                #Validation check
                self.get_unit_amount(line)
                amount_kg = self.get_total_kg(line)
                price_per_kg = total_price/amount_kg
                origin_country = self.get_origin_country(name)
                try:
                    category = self.get_category(id)
                    raw_goods = self.get_raw_goods(id)
                except NoCategoryError:
                    category = ""
                    raw_goods = ""
                rows.append([year,quarter,hospital,category,source,raw_goods,conv_or_eco,
                            variant,price_per_unit,total_price,amount_kg,price_per_kg,origin_country,None,None,None,None,None,None,None,None])
            except ValueError:
                pass
            
        return rows



    def import_dir(self,dir):
        files = listdir(dir)
        arr = []
        for filename in files:
            #The temp file created by excel when file is opened
            if '~$' in filename:
                continue
            res = self.import_data(dir,filename)
            arr = arr + res
        return arr
"""
