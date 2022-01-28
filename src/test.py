import pandas as pd
from import_files import import_excel

validation = import_excel('test1.xlsx').round(1)
test = import_excel('test2.xlsx').round(1)
headers = {'Hospital' : 2,'Leverandør' : 4,'Pris i alt' : 9,'Kg' : 10,'Kilopris' : 11,'Varianter / opr' : 7}

validation['Varianter / opr'] = validation['Varianter / opr'].map(lambda x: " ".join(x.split()))
validation['Hospital'] = validation['Hospital'].map(lambda x: " ".join(x.split()))
test['Hospital'] = test['Hospital'].map(lambda x: " ".join(x.split()))

def eps_compare(f1,f2):
    eps = 0.1
    if abs(f1-f2) <= eps:
        return True
    return False

for i in range(len(validation)):
    line = test.loc[i]
    df = validation
    manual = False
    for key,val in headers.items():
        value = line[val]
        if val > 7:
            value = float(value)
        df_new = df.loc[df[key] == value]
        if df_new.empty:
            print('HERE')
            print(df)
            print(key)
            print(i)
            print(line)
            inp = input()
            if inp == '':
                print('dropped')
                #print(i)
                index = df.index.to_list()[0]
                validation = validation.drop(index)
                manual = True
                break
        df = df_new
    if len(df) >= 1:
        #print(i)
        if manual:
            pass
        else:
            index = df.index.to_list()[0]
            validation = validation.drop(index)
    else:
        print('no match')