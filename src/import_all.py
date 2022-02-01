#dirs
import pandas as pd
from src.parsers.ac_import import AC_Import
from src.parsers.bc_import import BC_Import
from src.constants import BC, EM, GG, HK, CBP,COLUMN_NAMES, AC, DF, SG
from src.import_files import export_excel
from src.parsers.cbp_import import CBP_Import
from src.parsers.df_import import DF_Import
from src.parsers.em_import import EM_Import
from src.parsers.gg_import import GG_Import
from src.parsers.hk_import import HK_Import
from src.parsers.sg_import import SG_Import
"""
from src.parsers.em_import import EM_Import
from src.parsers.gg_import import GG_Import
from src.parsers.hk_import import HK_Import
from src.parsers.cbp_import import CBP_Import
from src.parsers.df_import import DF_Import
from src.parsers.sg_import import SG_Import
"""


ac_path = 'Specialisterne\\AC'
df_path = 'Specialisterne\\Dagrofa'
sg_path = 'Specialisterne\\Frisksnit'

#Files
bc_path = 'Specialisterne\\BC.xlsx'
em_path = 'Specialisterne\\Emmerys 01-04-2021..30-06-2021.xlsx'
gg_path = 'Specialisterne\\Grønt Grossisten.csv'
hk_path = 'Specialisterne\\Hørkram.xlsx'
cbp_path = 'Specialisterne\\CBP bageri.xlsx'

arr = []
ac = AC_Import()
res = ac.import_dir(ac_path)
arr = arr + res

bc = BC_Import()
res = bc.import_data(bc_path)
arr = arr + res

em = EM_Import(EM)
res = em.import_data(em_path)
arr = arr + res

gg = GG_Import(GG)
res = gg.import_data(gg_path)
arr = arr + res

hk = HK_Import(HK)
res = hk.import_data(hk_path)
arr = arr + res

cbp = CBP_Import()
res = cbp.import_data(cbp_path)
arr = arr + res



df = DF_Import(DF)
res = df.import_dir(df_path)
arr = arr + res

sg = SG_Import(SG)
res = sg.import_dir(sg_path)
arr = arr + res
"""
"""
resdf = pd.DataFrame(arr,columns = COLUMN_NAMES)
export_excel(resdf,'test.xlsx')