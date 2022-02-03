from calendar import c
import pandas as pd
from src.excel_file_functions import import_excel


def compare(test_df,validation_df,columns):
    correct = 0
    wrong = 0
    for i in range(len(test_df)):
        validation = validation_df
        line = test_df.loc[i]
        try:
            for column in columns:
                value = line[column]
                validation = column_value_exists(column,value,validation)
            drop_index = validation.index.to_list()
            validation= validation_df.drop(drop_index[0])
            correct += 1
        except ValueError:
            #print(line[:13])
            #input()
            wrong += 1
    print(correct,wrong)

def column_value_exists(column_name,column_val,df,reset=False):
    dfnew = df.loc[df[column_name] == column_val]
    if dfnew.empty:
        print(column_name)
        print(column_val)
        print(df.iloc[:,:9])
        print('next')
        raise ValueError()
    if reset:
        dfnew = dfnew.reset_index()
    return dfnew

def filterout(column_name,column_val,df):
    dfnew = df.loc[df[column_name] != column_val]
    return dfnew.reset_index()



validation = import_excel('test_data\\2021 K2 renset.xlsx',import_header=True).round(1)
test = import_excel('renset.xlsx',import_header=True).round(1)
test = filterout('Hospital','no_id',test)

headers = ['Hospital','Leverandør','Pris i alt','Kg','Kilopris','Varianter / opr']
validation['Hospital'] = validation['Hospital'].map(lambda x: " ".join(x.split()))

validation['Varianter / opr'] = validation['Varianter / opr'].map(lambda x: " ".join(x.split()))
test['Hospital'] = test['Hospital'].map(lambda x: " ".join(x.split()))


def ac_compare(validation,test,headers):
    valid = column_value_exists('Leverandør','AC',validation,True)
    test = column_value_exists('Leverandør','AC',test,True)
    compare(test,valid,headers)

def bc_compare(validation,test,headers):
    valid = column_value_exists('Leverandør','BC',validation,True)
    test = column_value_exists('Leverandør','BC',test,True)
    compare(test,valid,headers)

def df_compare(validation,test,headers):
    valid = column_value_exists('Leverandør','DF',validation,True)
    test = column_value_exists('Leverandør','DF',test,True)
    compare(test,valid,headers)

def em_compare(validation,test,headers):
    valid = column_value_exists('Leverandør','EM',validation,True)
    test = column_value_exists('Leverandør','EM',test,True)
    compare(test,valid,headers)

def gg_compare(validation,test,headers):
    valid = column_value_exists('Leverandør','GG',validation,True)
    test = column_value_exists('Leverandør','GG',test,True)
    compare(test,valid,headers)

def hk_compare(validation,test,headers):
    valid = column_value_exists('Leverandør','HK',validation,True)
    test = column_value_exists('Leverandør','HK',test,True)
    compare(test,valid,headers)

def sg_compare(validation,test,headers):
    def tailing_dash(x):
        if x[-1] == '-':
            return x[:-1].rstrip()
        else:
            return x.rstrip()
    valid = column_value_exists('Leverandør','SG',validation,True)
    valid['Varianter / opr'] = valid['Varianter / opr'].map(lambda x: tailing_dash(x))
    test = column_value_exists('Leverandør','SG',test,True)
    compare(test,valid,headers)

#ac_compare(validation,test,headers)
#bc_compare(validation,test,headers)
#df_compare(validation,test,headers)
#em_compare(validation,test,headers)
#gg_compare(validation,test,headers)
#hk_compare(validation,test,headers)
sg_compare(validation,test,headers)