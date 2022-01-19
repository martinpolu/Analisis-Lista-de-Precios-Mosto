import pdfplumber
import re
import pandas as pd
import locale
import pathlib

from Auxiliares import HallarDataframe,GenerarSQL
from datetime import datetime
from os import listdir

RelativePath=str(pathlib.Path(__file__).parent.resolve())
pd.set_option('display.max_rows',1600)
pd.set_option('display.max_columns',5)
locale.setlocale(locale.LC_ALL,'es_ES.UTF-8')
pagina=[]

print("Elija las listas de precios para comparar: ")
ListaDeArchivos=listdir((RelativePath)+"/PDF")
for f,item in enumerate(ListaDeArchivos):
    if(".pdf" in item):
        date_time_obj = datetime.strptime(item, '%Y%m%d Lista Distribucion.pdf')
        print(str(f)+date_time_obj.strftime('  Lista %d de %B %Y'))
        path=RelativePath+"/PDF/"+ListaDeArchivos[int(f)]
        print(path)
        Dataframe1= pd.DataFrame(HallarDataframe(path))
        GenerarSQL(Dataframe1)
