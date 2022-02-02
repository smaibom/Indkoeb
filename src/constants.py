
COLUMN_NAMES = ['År','Kvartal','Hospital','Råvarekategori','Leverandør','Råvare','konv/øko','Varianter / opr','Pris pr enhed','Pris i alt','Kg','Kilopris',
                'Oprindelse','Kg CO2-eq pr kg','Kg CO2-eq pr kg total','Kg CO2-eq pr MJ total','Kg CO2-eq pr g protein','Kg CO2-eq pr g protein total',
                'Arealanvendelse m2','Arealanvendelse m2 total','CO2 tal']

CATEGORY_INDEX = 3
RAW_GOODS_INDEX = 5
NAME_INDEX = 7

																		
PRICE_PER_UNIT = {'ac' : 'Pris pr. Enhed', 'gg' : 11}
TOTAL_PRICE = {'ac' : 'Pris i alt', 'gg' : 12, 'sg' : 5}
TOTAL_WEIGHT = {'ac' : 'Netto kg', 'gg' : 7, 'sg' : 4}
TOTAL_UNITS = {'ac' : 'Antal Enheder', 'sg' : 3}

HOSPITALS_TRANSLATE_FILE_PATH = 'StatiskData\\hospitals.xlsx'
CATEGORY_FILE_PATH = 'StatiskData\\categories.xlsx'
CATEGORY_FILE_HEADERS = ['ID','Råvarekategori','Råvare']

GG_CSV_HEADERS = ['Source No','Item No','ItemDescription','UnitOfMeasure','Quantity','Amount',
                  'NettoWeight','TotalWeight','Ecology','Oprindelse', 'empty','Pris pr enhed',
                  'Pris i alt']


AC_HEADERS = ['Kundenr','Kundenavn','Varenr','Varebeskrivelse','Antal Enheder','Netto kg','Pris i alt','Pris pr. Enhed']
AC = {'headers' : AC_HEADERS, 'year' : 2021, 'quarter' : 'K2', 'source' : 'AC','total_price_index' : 6, 'total_weight_index' :5 ,
      'units_index' : 4, 'price_per_unit_index' : 7} 

BC_HEADERS = ['Varenr.','Beskrivelse','Mærke','Basisenhed','Enhed','Antal','Beløb','Beløb pr. antal',
              'Øko KG','Konv KG','Udeholdt KG','','','','','','Oprindelse','Produktionsland','P.Hovedgruppe','P.Undergruppe']
BC = {'headers' : BC_HEADERS, 'year' : 2021, 'quarter' : 'K2', 'source' : 'BC','total_price_index' : 6, 'total_weight_eco_index' : 8,
      'total_weight_konv_index' : 9,'total_weight_unknown_index' : 10, 'units_index' : 5, 'price_per_unit_index' : 7, 'file_start' : 3} 

DF_HEADERS = ['Varenr.','Varenavn']
DF = {'headers' : DF_HEADERS, 'file_start' : 6, 'year' : 2021, 'quarter' : 'K2', 'source' : 'DF'}

GG_HEADERS = ['Source No_','Item No_','ItemDescription','UnitOfMeasure','Quantity']
GG = {'headers': GG_HEADERS, 'year' : 2021, 'quarter' : 'K2', 'source' : 'GG','total_price_index' : 12, 
        'total_weight_index' : 7 ,'units_index' : 4, 'price_per_unit_index' : 11} 

SG_HEADERS = ['Gruppe','Nr.','Navn']
SG = {'headers' : SG_HEADERS, 'file_start' : 2, 'year' : 2021, 'quarter' : 'K2', 'source' : 'SG', 'total_price_index' : 5, 
      'total_weight_index' : 4,'units_index' : 3} 

HK_HEADERS = ['Kd-nr.','FA','Art.-nr.']
HK = {'headers' : HK_HEADERS, 'file_start': 1, 'year' : 2021, 'quarter' : 'K2', 'source' : 'HK','total_price_index' : 10,
    'total_weight_index' : 12,'units_index' : 9}


CBP_HEADERS = ['Kunder - Kunde nr og Navn','Produkter - Vare nr & Navn.','Mængde (kg)','Omsætning']
CBP =  {'headers' : CBP_HEADERS, 'year' : 2021, 'quarter' : 'K2', 'source' : 'CBP', 'total_price_index' : 3,'total_weight_index' :2}


EM_HEADERS = ['Lokation:']
EM = {'headers': EM_HEADERS, 'year' : 2021, 'quarter' : 'K2', 'source' : 'EM', 'total_price_index' : 4, 'total_weight_index' : 6,'price_per_unit_index' : 2}
