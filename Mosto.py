import pdfplumber
import re
import pandas as pd
import locale
from datetime import datetime
from os import listdir
pd.set_option('display.max_rows',1600)
pd.set_option('display.max_columns',5)
locale.setlocale(locale.LC_ALL,'es_ES.UTF-8')
separador = "\n"
pagina=[]
dict=[]

print("Elija la lista de precios para comparar: ")
for f,item in enumerate(listdir("PDF")):
    if(".pdf" in item):
        date_time_obj = datetime.strptime(item, '%Y%m%d Lista Distribucion.pdf')
        print(str(f)+date_time_obj.strftime('  Lista %d de %B %Y'))
opcion=input()
opcion2=input()
path="PDF\\"+listdir("PDF")[int(opcion)]
path2="PDF\\"+listdir("PDF")[int(opcion2)]
# Lista 6 primera de 2021
with pdfplumber.open(path) as pdf:
    for i in range(len(pdf.pages)):
        pagina = pdf.pages[i]
        lista = pagina.extract_text().split(separador)
        for j in range(len(lista)):
            pattern="Fecha: [0-9]+/+[0-9]+/[0-9]+"
            FechaProv1 = re.search(pattern, lista[j])
            if FechaProv1:
                Fecha1 = datetime.strptime((FechaProv1.group(0)), 'Fecha: %d/%m/%Y')
            pattern = re.compile("[0-9]+.+  [0-9,.]+")
            if(pattern.match(lista[j]))!=None:
                a=(re.findall("[0-9]+",lista[j]))
                codigo=a[0]
                linearecor=lista[j][len(a[0])+1:]
                linearecor=linearecor.split("  ")
                if(len(linearecor)>2):
                    linearecor1=["",""]
                    for k in range(len(linearecor)-1):
                        linearecor1[0]=linearecor1[0]+linearecor[k]+" "
                    linearecor1[1]=linearecor[len(linearecor)-1].replace(",","")
                    linearecor=linearecor1
                else:
                    linearecor[1]=linearecor[1].replace(",","")
                dict.append({"Producto":(linearecor)[0],"Precio "+Fecha1.strftime('%d de %B %Y'):float(linearecor[1])})
Dataframe1= pd.DataFrame(dict)
dict=[]

with pdfplumber.open(path2) as pdf:
    for i in range(len(pdf.pages)):
        pagina = pdf.pages[i]
        lista = pagina.extract_text().split(separador)
        for j in range(len(lista)):
            pattern="Fecha: [0-9]+/+[0-9]+/[0-9]+"
            FechaProv1 = re.search(pattern, lista[j])
            if FechaProv1:
                Fecha1 = datetime.strptime((FechaProv1.group(0)), 'Fecha: %d/%m/%Y')
            pattern = re.compile("[0-9]+.+  [0-9,.]+")
            if(pattern.match(lista[j]))!=None:
                a=(re.findall("[0-9]+",lista[j]))
                codigo=a[0]
                linearecor=lista[j][len(a[0])+1:]
                linearecor=linearecor.split("  ")
                if(len(linearecor)>2):
                    linearecor1=["",""]
                    for k in range(len(linearecor)-1):
                        linearecor1[0]=linearecor1[0]+linearecor[k]+" "
                    linearecor1[1]=linearecor[len(linearecor)-1].replace(",","")
                    linearecor=linearecor1
                else:
                    linearecor[1]=linearecor[1].replace(",","")
                dict.append({"Producto":(linearecor)[0],"Precio "+Fecha1.strftime('%d de %B %Y'):float(linearecor[1])})
Dataframe2= pd.DataFrame(dict)
Dataframe1.set_index('Producto',inplace=True)
Dataframe2.set_index('Producto',inplace=True)
result = pd.concat([Dataframe1, Dataframe2], axis=1, join="inner")
result["Aumento"]=(result[str(result.columns[1])])/(result[str(result.columns[0])])
result.sort_values(by=['Aumento'],inplace=True,ascending=False)
result.to_excel("PDF\\"+listdir("PDF")[int(opcion)][:-4]+".xlsx")
