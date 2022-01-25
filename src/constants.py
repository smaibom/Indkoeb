COLUMN_NAMES = ['År','Kvartal','Hospital','Råvarekategori','Leverandør','Råvare','konv/øko','Varianter / opr','Pris pr enhed','Pris i alt','Kg','Kilopris',
                'Oprindelse','Kg CO2-eq pr kg','Kg CO2-eq pr kg total','Kg CO2-eq pr MJ total','Kg CO2-eq pr g protein','Kg CO2-eq pr g protein total',
                'Arealanvendelse m2','Arealanvendelse m2 total','CO2 tal']

AC_CLIENT_HOSPITAL_HEADERS = ['Kundenr','Hospital']
AC_YEAR = 2021
AC_QUARTER = 'K2'
AC_SOURCE = 'AC'
																		
PRICE_PER_UNIT = {'ac' : 'Pris pr. Enhed'}
TOTAL_PRICE = {'ac' : 'Pris i alt'}
TOTAL_WEIGHT = {'ac' : 'Netto kg'}
TOTAL_UNITS = {'ac' : 'Antal Enheder'}


GG_HEADERS = ['Source No','Item No','ItemDescription','UnitOfMeasure','Quantity','Amount','NettoWeight','TotalWeight','Ecology','Oprindelse', 'empty','Pris pr enhed',
              'Pris i alt']
GG_YEAR = 2021
GG_QUARTER = 'K2'
GG_SOURCE = 'GG'
GG_HOSPITALS = {'Rigshospitalet Glostrup' : 'RHG centralkøkken', 'Rigshospitalet Centralkøkken' : 'RH centralkøkken',
                'Rigshospitalet Kantinen ME-EAT' : 'RH kantine', 'Bornholms Hospital' : 'BOH'}
