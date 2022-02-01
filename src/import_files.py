import pandas as pd

from src.constants import COLUMN_NAMES, PRICE_PER_UNIT, TOTAL_PRICE,HOSPITALS_TRANSLATE_FILE_PATH


def import_excel(filepath,skiprow = 0):
    return pd.read_excel(filepath,skiprows = skiprow,header=None)

def import_excel_with_headers(filepath):
    return pd.read_excel(filepath)

def import_csv(filepath,headers):
    return pd.read_csv(filepath, sep=';', encoding='latin-1',names = headers)

def export_excel(df, filename):
    with pd.ExcelWriter(filename,engine='xlsxwriter') as writer:
        df.to_excel(excel_writer=writer, sheet_name='Filter', index=False)
        worksheet = writer.sheets['Filter']
        # set up autofilter
        worksheet.autofilter(0, 0, len(df.index) - 1, len(df.columns) - 1)

def import_excel_sheet(filepath,sheet):
    xls = pd.ExcelFile(filepath)
    return pd.read_excel(xls, sheet)

def get_excel_sheet_names(filepath):
    xls = pd.ExcelFile(filepath)
    return xls.sheet_names

def clear_duplicates():
    a = import_excel('temp.xlsx')
    a = a.drop_duplicates('ID')
    export_excel(a,'noduplicates.xlsx')
#clear_duplicates()
data = []

#print(import_excel_sheet(HOSPITALS_TRANSLATE_FILE_PATH,'ac'))
"""



df1 = import_excel('test1.xlsx')
df2 = import_excel('test2.xlsx')
for i in range(len(df1)):
    for j in range(13):
        try:
            item1 = df1.iloc[i,j].rstrip()
            item2 = df2.iloc[i,j].rstrip()
        except:
            try:
                item1 = round(df1.iloc[i,j])
                item2 = round(df2.iloc[i,j])
            except:
                print(i+2)
        if item1 != item2:
            print(df1.iloc[i,j])
            print(df2.iloc[i,j])
            print('row')
            print(i+2)
            print('column')
            print(j)
            raise ValueError()
"""