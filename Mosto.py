import pdfplumber
import re
import pandas as pd
import locale
import pathlib
from Auxiliares import HallarDataframe
from datetime import datetime
from os import listdir


RelativePath=str(pathlib.Path(__file__).parent.resolve())



pd.set_option('display.max_rows',1600)
pd.set_option('display.max_columns',5)
locale.setlocale(locale.LC_ALL,'es_ES.UTF-8')
separador = "\n"
pagina=[]

print("Elija las listas de precios para comparar: ")
ListaDeArchivos=listdir((RelativePath)+"/PDF")
for f,item in enumerate(ListaDeArchivos):
    if(".pdf" in item):
        date_time_obj = datetime.strptime(item, '%Y%m%d Lista Distribucion.pdf')
        print(str(f)+date_time_obj.strftime('  Lista %d de %B %Y'))
opcion=input()
opcion2=input()
path=RelativePath+"/PDF/"+ListaDeArchivos[int(opcion)]
path2=RelativePath+"/PDF/"+ListaDeArchivos[int(opcion2)]
print(path)
# Lista 6 primera de 2021


Dataframe1= pd.DataFrame(HallarDataframe(path))
Dataframe2= pd.DataFrame(HallarDataframe(path2))

Dataframe1.set_index('Producto',inplace=True)
Dataframe2.set_index('Producto',inplace=True)
result = pd.concat([Dataframe1, Dataframe2], axis=1, join="inner")
result["Aumento"]=(result[str(result.columns[1])])/(result[str(result.columns[0])])
result.sort_values(by=['Aumento'],inplace=True,ascending=False)
result.to_excel(RelativePath+"/PDF/Comparativa.xlsx")
