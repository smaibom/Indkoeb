import os
from openpyxl import load_workbook
import pandas as pd

from src.constants import COLUMN_NAMES, PRICE_PER_UNIT, TOTAL_PRICE,HOSPITALS_TRANSLATE_FILE_PATH



def import_csv(filepath,headers):
    """
    Imports a csv file

    args:
        filepath: Filepath to the csv file
        headers: Headers of the csv file
    returns:
        DataFrame of the CSV file
    """
    return pd.read_csv(filepath, sep=';', encoding='latin-1',names = headers)

def export_excel(df, filename):
    with pd.ExcelWriter(filename,engine='xlsxwriter') as writer:
        df.to_excel(excel_writer=writer, sheet_name='Filter', index=False)
        worksheet = writer.sheets['Filter']
        # set up autofilter
        worksheet.autofilter(0, 0, len(df.index) - 1, len(df.columns) - 1)

def import_excel_sheet(filepath,sheet,skiprow = 0, import_header=False):
    """
    Imports a specific excel sheet from a given filepath
    args:
        filepath: Filepath to the excel file
        sheet: Sheet name of the sheet being opened
        skiprow: How many rows should be skipped in the excel file, defaults to 0
        import_header: Boolean of if first line should be seen as the headers of the pandas file, defaults to false
    returns:
        DataFrame with the excel sheet data
    """
    xls = pd.ExcelFile(filepath)
    if import_header:
        df = pd.read_excel(xls, sheet,skiprows = skiprow)
    else:
        df = pd.read_excel(xls, sheet,skiprows = skiprow, header = None)
    return df

def import_excel(filepath,skiprow = 0, import_header=False):
    """
    Imports an excel file from a given filepath
    args:
        filepath: Filepath to the excel file
        skiprow: How many rows should be skipped in the excel file, defaults to 0
        import_header: Boolean of if first line should be seen as the headers of the pandas file, defaults to false
    returns:
        DataFrame with the excel data
    """
    if import_header:
        df = pd.read_excel(filepath,skiprows = skiprow)
    else:
        df = pd.read_excel(filepath,skiprows = skiprow, header = None)
    return df

def get_excel_sheet_names(filepath):
    """
    Gets excel sheet names in an excel file
    returns:
        array of string names for each sheet in file
    """
    xls = pd.ExcelFile(filepath)
    return xls.sheet_names

def write_sheets_to_excel_file(filename,sheet_df_data):
    writer = pd.ExcelWriter(filename, engine='openpyxl')
    #Write each sheet to the writer
    for (sheet,df) in sheet_df_data.items():
        df.to_excel(writer, sheet_name = sheet,index=False)
    #Save
    writer.save()

def append_df_to_excel(filename,sheet_df_data):
    """
    Appends data to a given filename, if filename dosent exist it is created with available data
    args:
        filename: Filepath to the excel sheet
        sheet_df_data: A dictionary with entries of {sheet_name : dataframe with data for sheet}
    """
    if not os.path.isfile(filename):
        #Create the writer for writing multiple sheets
        writer = pd.ExcelWriter(filename, engine='openpyxl')
        #Write each sheet to the writer
        for (sheet,df) in sheet_df_data.items():
            df.to_excel(writer, sheet_name = sheet,index=False)
        #Save
        writer.save()
        return
    
    #Create the writer for writing multiple sheets
    writer = pd.ExcelWriter(filename, engine='openpyxl', mode='a')

    #Open exisiting data into writer
    writer.book = load_workbook(filename)

    #Get original data 
    writer.sheets = {ws.title:ws for ws in writer.book.worksheets}
    # write out the new sheet
    for (sheet,df) in sheet_df_data.items():
        df.to_excel(writer, sheet,index=False)

    # save the workbook
    writer.save()

