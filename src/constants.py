COLUMN_NAMES = ['År','Kvartal','Hospital','Råvarekategori','Leverandør','Råvare','konv/øko','Varianter / opr','Pris pr enhed','Pris i alt','Kg','Kilopris',
                'Oprindelse','Kg CO2-eq pr kg','Kg CO2-eq pr kg total','Kg CO2-eq pr MJ total','Kg CO2-eq pr g protein','Kg CO2-eq pr g protein total',
                'Arealanvendelse m2','Arealanvendelse m2 total','CO2 tal']

AC_CLIENT_HOSPITAL_HEADERS = ['Kundenr','Hospital']
AC_YEAR = 2021
AC_QUARTER = 'K2'
AC_SOURCE = 'AC'
																		
PRICE_PER_UNIT = {'ac' : 'Pris pr. Enhed', 'gg' : 11}
TOTAL_PRICE = {'ac' : 'Pris i alt', 'gg' : 12, 'sg' : 5}
TOTAL_WEIGHT = {'ac' : 'Netto kg', 'gg' : 7, 'sg' : 4}
TOTAL_UNITS = {'ac' : 'Antal Enheder', 'sg' : 3}

HOSPITALS_TRANSLATE_FILE_PATH = 'StatiskData\\hospitals.xlsx'
CATEGORY_FILE_PATH = 'StatiskData\\categories.xlsx'

GG_HEADERS = ['Source No','Item No','ItemDescription','UnitOfMeasure','Quantity','Amount','NettoWeight','TotalWeight','Ecology','Oprindelse', 'empty','Pris pr enhed',
              'Pris i alt']
GG_YEAR = 2021
GG_QUARTER = 'K2'
GG_SOURCE = 'GG'
GG_HOSPITALS = {'Rigshospitalet Glostrup' : 'RHG centralkøkken', 'Rigshospitalet Centralkøkken' : 'RH centralkøkken',
                'Rigshospitalet Kantinen ME-EAT' : 'RH kantine', 'Bornholms Hospital' : 'BOH'}


SG_HOSPITALS = {'BBH' : 'BBH', 'RH' : 'RH centralkøkken', 'RH2' : 'RH kantine', 'BOH' : 'BOH', 'HIH' : 'NOH centralkøkken', 'GLO' : 'RHG centralkøkken'}

AC = {'year' : 2021, 'quarter' : 'K2', 'source' : 'AC','total_price_index' : 6, 'total_weight_index' :5 ,'units_index' : 4, 'price_per_unit_index' : 7} #DONE
DF = {'year' : 2021, 'quarter' : 'K2', 'source' : 'DF'}
HK = {'year' : 2021, 'quarter' : 'K2', 'source' : 'HK','total_price_index' : 10,'total_weight_index' : 12,'units_index' : 9}
SG = {'year' : 2021, 'quarter' : 'K2', 'source' : 'SG', 'total_price_index' : 5, 'total_weight_index' : 4,'units_index' : 3} #DONE
GG = {'year' : 2021, 'quarter' : 'K2', 'source' : 'GG','total_price_index' : 12, 'total_weight_index' : 7 ,'units_index' : 4, 'price_per_unit_index' : 11} #DONE
BC = {'year' : 2021, 'quarter' : 'K2', 'source' : 'BC','total_price_index' : 6, 'total_weight_eco_index' : 8,'total_weight_konv_index' : 9,'total_weight_unknown_index' : 10, 'units_index' : 5, 'price_per_unit_index' : 7} 
EM = {'year' : 2021, 'quarter' : 'K2', 'source' : 'EM', 'total_price_index' : 4, 'total_weight_index' : 6,'price_per_unit_index' : 2}
CBP =  {'year' : 2021, 'quarter' : 'K2', 'source' : 'CBP', 'total_price_index' : 3,'total_weight_index' :2}