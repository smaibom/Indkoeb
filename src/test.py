import pandas as pd
from import_files import import_excel

file1 = import_excel('test1.xlsx')
file2 = import_excel('test2.xlsx')

def eps_compare(f1,f2):
    eps = 0.1
    if abs(f1-f2) <= eps:
        return True
    return False

for i in range(len(file1)):
    f1line = file1.loc[i]
    f2line = file2.loc[i]
    for j in range(len(f1line)):
        if pd.isna(f1line[j]) and pd.isna(f2line[j]):
            continue
        if j == 11 or j == 10 or j == 8:
            if not eps_compare(f1line[j],f2line[j]):
                print('row %s column %s' % (i+2,j+1))
                print(f1line[j],f2line[j])
                raise ValueError
        elif f1line[j] != f2line[j]:
            print('row %s column %s' % (i+2,j+1))
            print(f1line[j],f2line[j])
            raise ValueError