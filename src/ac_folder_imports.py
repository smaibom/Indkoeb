from constants import AC_CLIENT_HOSPITAL_HEADERS, AC_QUARTER, AC_SOURCE, AC_YEAR, COLUMN_NAMES, PRICE_PER_UNIT, TOTAL_PRICE, TOTAL_UNITS, TOTAL_WEIGHT
import re
from os import listdir
import pandas as pd
from import_files import export_excel, import_excel


def get_year():
    """
    Returns the year for the AC files, it dosent exist in file and is just a constant
    """
    return AC_YEAR

def get_quarter():
    """
    Returns the quarter for the AC files, it dosent exist in file and is just a constant
    """
    return AC_QUARTER


def get_hospital_nr_from_filename(filename):
    """
    Splits a AC filename and takes the client number 
    A file in the AC folder follows the format of '<clientnumber> <hospital information>' The end part of the hopsital information 
    is not consistant but the client number is always first seperated by a space so we only use that information
    """
    #Its always the first element of the filename
    number = filename.split(' ')[0]
    return number

def get_hospital_from_number(df,client_number):
    """
    Takes a client number from a file in the ac folder and translate it into the desired clientname.

    args:
        df: A dataframe with 2 columns, Kundenr and Hospital
        client_number: Int value with the client number
    returns: 
        A string with the Hospital name
    """
    client_nr = AC_CLIENT_HOSPITAL_HEADERS[0]
    df = df.loc[df[client_nr] == int(client_number)]
    return df.iloc[0,1]

def get_category(df):
    """
    Gets the category of a good from a file that has a id of the item with the catagory/type of the good
    args:
        df: The dataframe of the item already searched for
    returns:
        String value with the name of the category, empty string if no entry is found
    """
    if df.empty:
        return ""
    #ID is unique, category is in row 1
    category = df.iloc[0,1]
    return category

def get_item_from_id(df,id):
    return df.loc[df['ID'] == id]

def get_source():
    return AC_SOURCE

def get_origin_country(description):
    """
    The origin country in a AC 
    """
    pass

def get_food_type(description):
    if 'ØKO' in description:
        return 'Øko'
    return 'Konv'

def get_unit_amount(index,df):
    column_loc = df.columns.get_loc(TOTAL_UNITS['ac'])
    val = df.iloc[index,column_loc]
    if val == 0:
        raise ValueError()
    return val

def get_kg_amount(index,df):
    column_loc = df.columns.get_loc(TOTAL_WEIGHT['ac'])
    val = df.iloc[index,column_loc]
    if val == 0:
        raise ValueError()
    return val

def get_price_per_unit(df,index):
    price_per_unit_column_number = df.columns.get_loc(PRICE_PER_UNIT['ac'])
    return df.iloc[index,price_per_unit_column_number]

def get_total_price(df,index):
    total_price_column_number = df.columns.get_loc(TOTAL_PRICE['ac'])
    return df.iloc[index,total_price_column_number]

def get_variant(name):
    """
    Names in files are listed as "ØKO item (country)" ØKO is optional
    """
    name = name.rstrip()
    if 'ØKO' in name:
        name = name[4:]
    name = name.split('(')[0]
    return " ".join(name.split())

def get_origin_country(name):
    if '(0)' in name:
        raise ValueError('Not valid country')
    try:
        name = name.rstrip().split('(')[1].split(')')[0]
    except:
        return ""
    if len(name) <2 or len(name) > 5:
        return ""
    return name



def get_raw_goods(df):
    if df.empty:
        return ""
    raw_goods = df.iloc[0,2]
    return raw_goods

def get_data_from_ac_file(dir,filename):
    df = import_excel(dir + '\\' + filename)
    dfh = import_excel('C:\\Users\\KOM\\Documents\\Indkoeb\\StatiskData\\Hospitaler.xlsx')
    df_id = import_excel('C:\\Users\\KOM\\Documents\\Indkoeb\\StatiskData\\id-type.xlsx')

    year = get_year()
    quarter = get_quarter()

    client_nr = get_hospital_nr_from_filename(filename)
    hospital = get_hospital_from_number(dfh,client_nr)

    source = get_source()

    
    
    rows = []
    for i in range(len(df)):
        try:
            id = df.iloc[i,2]
            item = get_item_from_id(df_id,id)
            name = df.iloc[i,3]
            conv_or_eco = get_food_type(name)
            variant = get_variant(name)
            price_per_unit = get_price_per_unit(df,i)
            total_price = get_total_price(df,i)
            category = get_category(item)
            raw_goods = get_raw_goods(item)
            #Validation check
            get_unit_amount(i,df)
            amount_kg = get_kg_amount(i,df)
            price_per_kg = total_price/amount_kg
            origin_country = get_origin_country(name)
            rows.append([year,quarter,hospital,category,source,raw_goods,conv_or_eco,
                        variant,price_per_unit,total_price,amount_kg,price_per_kg,origin_country,None,None,None,None,None,None,None,None])
        except ValueError:
            pass
    return rows



def import_all_files_ac(dir):
    files = listdir(dir)
    arr = []
    for filename in files:
        #The temp file created by excel when file is opened
        if '~$' in filename:
            continue
        res = get_data_from_ac_file(dir,filename)
        arr = arr + res
    res = pd.DataFrame(arr,columns = COLUMN_NAMES)
    export_excel(res,'test.xlsx')

p = 'C:\\Users\\KOM\\Documents\\Indkoeb\\Specialisterne\\AC\\Ny mappe'
import_all_files_ac(p)