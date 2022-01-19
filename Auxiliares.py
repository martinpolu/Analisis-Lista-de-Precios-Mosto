import pdfplumber
import re
import sqlite3
import pathlib
import pandas as pd


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
                    if(Fecha1<datetime(2021,11,4)):
                        producto=linearecor[1:59]
                        producto=producto.split("   ")
                        producto=producto[0]
                        precio=linearecor[58:70]
                        precio=float(precio.replace(",","."))
                        proveedor=linearecor[70:]
                        dict.append({"Producto":producto,Fecha1.strftime('%d/%m/%Y'):precio})
                    if(Fecha1<datetime(2021,11,30) and Fecha1>datetime(2021,11,5)):
                        linearecor=linearecor.split("  ")
                        if(len(linearecor)>2):
                            linearecor1=["",""]
                            for k in range(len(linearecor)-1):
                                linearecor1[0]=linearecor1[0]+linearecor[k]+" "
                            linearecor1[1]=linearecor[len(linearecor)-1].replace(",","")
                            linearecor=linearecor1
                        else:
                            linearecor[1]=linearecor[1].replace(",","")
                        # print(linearecor)
                        dict.append({"Producto":(linearecor)[0][:-4],Fecha1.strftime('%d/%m/%Y'):float(linearecor[1])})

                    if(Fecha1>datetime(2021,11,30)):
                        linearecor=linearecor.split("  ")
                        if(len(linearecor)>2):
                            linearecor1=["",""]
                            for k in range(len(linearecor)-1):
                                linearecor1[0]=linearecor1[0]+linearecor[k]+" "
                            linearecor1[1]=linearecor[len(linearecor)-1].replace(",","")
                            linearecor=linearecor1
                        else:
                            linearecor[1]=linearecor[1].replace(",","")
                        # print(linearecor)
                        dict.append({"Producto":(linearecor)[0],Fecha1.strftime('%d/%m/%Y'):float(linearecor[1])})

    return dict



def GenerarSQL(Listado):
    Columnas=[]
    conn = sqlite3.connect(RelativePath+"/PDF/ListaDePrecios.db")
    c = conn.cursor()

    c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='stocks' ''')

    #if the count is 1, then table exists
    if c.fetchone()[0]==1 :
        print('La tabla ahora hay que chequear si la columna ya existe en la tabla')
        print(list(Listado.columns.values)[1])
        cursor=c.execute('''SELECT * FROM stocks''')
        for column in cursor.description:
            Columnas.append(column[0])
        print(Columnas)
        cursor = c.execute('select * from stocks')
        if(not list(Listado.columns.values)[1] in Columnas):
            print("No esta la fecha en la columna")
            cols = [column[0] for column in cursor.description]
            results = pd.DataFrame.from_records(data = cursor.fetchall(), columns = cols)
            results.set_index('Producto',inplace=True)
            Listado.set_index('Producto',inplace=True)
            result = pd.concat([results, Listado], axis=1, join="outer")
            result.to_sql(name='stocks', con=conn, if_exists='replace', index=True)
        else:
            print("Si existia, entonces no hacemos nada.")
    else:
        print("La tabla no existe, debemos crearla con el dataframe.")
        Listado.to_sql(name='stocks', con=conn, if_exists='replace', index=False)
    conn.commit()
