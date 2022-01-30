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

ListaDeArchivos=listdir((RelativePath)+"/PDF")
for f,item in enumerate(ListaDeArchivos):
    if(".pdf" in item):
        date_time_obj = datetime.strptime(item, '%Y%m%d Lista Distribucion.pdf') #Identifica la fecha de la lista de precios.
        print(str(f)+date_time_obj.strftime('  Lista %d de %B %Y')) #Muestra la fecha de la lista de precios.
        path=RelativePath+"/PDF/"+ListaDeArchivos[int(f)] #Genera el path del archivo para leer
        print(path)
        Dataframe1= pd.DataFrame(HallarDataframe(path)) #Genera el dataframe de la lista de precios que está analizando.
        GenerarSQL(Dataframe1)
