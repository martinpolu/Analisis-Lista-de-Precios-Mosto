import pdfplumber
import re
import pandas as pd
from datetime import datetime
pd.set_option('display.max_rows',1600)
pd.set_option('display.max_columns',5)
separador = "\n"
pagina=[]
dict=[]

path=r'PDF\20220104 Lista Distribucion.pdf'
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
                dict.append({"Producto":(linearecor)[0],"Precio":float(linearecor[1])})
Dataframe1= pd.DataFrame(dict)
Dataframe1.to_excel("PDF\output1.xlsx")
