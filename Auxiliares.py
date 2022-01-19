import pdfplumber
import re
import sqlite3
import pathlib


RelativePath=str(pathlib.Path(__file__).parent.resolve())
from datetime import datetime

separador = "\n"


def HallarDataframe(path):
    dict=[]
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
                    if(Fecha1<datetime(2021,11,2)):
                        producto=linearecor[1:59]
                        producto=producto.split("   ")
                        producto=producto[0]
                        precio=linearecor[58:70]
                        precio=float(precio.replace(",","."))
                        proveedor=linearecor[70:]
                        # print(precio)
                        # print(proveedor)
                        dict.append({"Producto":producto,Fecha1.strftime('%d/%m/%Y'):precio})
                    else:
                        if(len(linearecor)>2):
                            linearecor1=["",""]
                            for k in range(len(linearecor)-1):
                                linearecor1[0]=linearecor1[0]+linearecor[k]+" "
                            linearecor1[1]=linearecor[len(linearecor)-1].replace(",","")
                            linearecor=linearecor1
                        else:
                            linearecor[1]=linearecor[1].replace(",","")
                        print(linearecor)
                        dict.append({"Producto":(linearecor)[0],Fecha1.strftime('%d/%m/%Y'):float(linearecor[1])})
    return dict



def GenerarSQL(Listado):
    print(Listado)
    conn = sqlite3.connect(RelativePath+"/PDF/ListaDePrecios.db")
    c = conn.cursor()
    cursor = c.execute('select * from stocks')
    for column in cursor.description:
        print(column[0])
    conn.commit()
