import pdfplumber
import re
import sqlite3
import pathlib
import pandas as pd
import datetime

RelativePath=str(pathlib.Path(__file__).parent.resolve())
from datetime import datetime

separador = "\n"

def checkKey(dic, key):
    if key in dic.keys():
        print("Present, ", end =" ")
        print("value =", dic[key])
    else:
        print("Not present")


def HallarDataframe(path):
    dict=[]
    patternFecha="Fecha: [0-9]+/+[0-9]+/[0-9]+" #Buscamos la fecha dentro de la lista de precios
    FechaProv1=0
    with pdfplumber.open(path) as pdf:
        for i in range(len(pdf.pages)): #Leemos todas las páginas
            pagina = pdf.pages[i]
            lista = pagina.extract_text().split(separador) #Leemos cada pagina utilizando como separador el salto de linea
            for j in range(len(lista)):
                if FechaProv1==0:
                    FechaProv2 = re.search(patternFecha, lista[j])
                    if FechaProv2:
                        FechaProv1=1
                        Fecha1 = datetime.strptime((FechaProv2.group(0)), 'Fecha: %d/%m/%Y')#Asignamos la fecha
                pattern = re.compile("[0-9]+.+  [0-9,.]+")#Buscamos el formato de producto y precio dentro de la lista.
                if(pattern.match(lista[j]))!=None:
                    ##a=(re.findall("[0-9]+",lista[j]))
                    ##linearecor=lista[j][len(a[0])+1:]
                    linearecor=lista[j][5:]
                    if(Fecha1<datetime(2021,11,4)):
                        # print("CASO A") #Este caso es para la primera lista de precios
                        producto=linearecor[1:59].split("   ")[0]
                        precio=float(linearecor[58:70].replace(",","."))
                        dict.append({"Producto":producto,Fecha1.strftime('%d/%m/%Y'):precio})
                    if(Fecha1<datetime(2021,11,30) and Fecha1>datetime(2021,11,5)):
                        # print("CASO B")
                        linearecor=linearecor.split("  ")
                        if(len(linearecor)>2):
                            linearecor1=["",""]
                            for k in range(len(linearecor)-2):
                                linearecor1[0]=linearecor1[0]+linearecor[k]+" "
                            linearecor1[0]=linearecor1[0]+linearecor[k+1]
                            linearecor1[1]=linearecor[len(linearecor)-1].replace(",","")
                            linearecor=linearecor1
                        else:
                            linearecor[1]=linearecor[1].replace(",","")
                        # print(linearecor)
                        dict.append({"Producto":(linearecor)[0][:-4],Fecha1.strftime('%d/%m/%Y'):float(linearecor[1])})

                    if(Fecha1>datetime(2021,11,30)):
                        # print("CASO C")
                        linearecor=linearecor.split("  ")
                        if(len(linearecor)>2):
                            linearecor1=["",""]
                            for k in range(len(linearecor)-2):
                                linearecor1[0]=linearecor1[0]+linearecor[k]+" "
                            linearecor1[0]=linearecor1[0]+linearecor[k+1]
                            linearecor1[1]=linearecor[len(linearecor)-1].replace(",","")
                            linearecor=linearecor1
                        else:
                            linearecor[1]=linearecor[1].replace(",","")
                        if not any(d['Producto'] == linearecor[0] for d in dict):
                            dict.append({"Producto":(linearecor)[0],Fecha1.strftime('%d/%m/%Y'):float(linearecor[1])})
    return dict



def GenerarSQL(Listado):
    Columnas=[]
    conn = sqlite3.connect(RelativePath+"/PDF/ListaDePrecios.db")
    c = conn.cursor()
    c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='stocks' ''')
    #if the count is 1, then table exists
    if c.fetchone()[0]==1 :
        print(list(Listado.columns.values)[1])
        cursor=c.execute('''SELECT * FROM stocks''')
        for column in cursor.description:
            Columnas.append(column[0])
        Columnas=Columnas[1:]
        sorted(Columnas, key=lambda x: datetime.strptime(x, '%d/%m/%Y'))
        Columnas.insert(0,"Producto")
        cursor = c.execute('select * from stocks')
        if(not list(Listado.columns.values)[1] in Columnas):
            print("No esta la fecha en la columna")
            cols = [column[0] for column in cursor.description]
            results = pd.DataFrame.from_records(data = cursor.fetchall(), columns = cols)
            results.set_index('Producto',inplace=True)
            Listado.set_index('Producto',inplace=True)
            result = pd.merge(results, Listado, how="outer", on=["Producto"])
            # result = pd.concat([results, Listado], axis=1, join="outer")
            # print(result)
            result.to_sql(name='stocks', con=conn, if_exists='replace', index=True)
        else:
            cursor = c.execute('select Producto, "'+list(Listado.columns.values)[1]+'" from stocks')
            cols=["Producto",list(Listado.columns.values)[1]]
            results = pd.DataFrame.from_records(data = cursor.fetchall(), columns = cols)
            results=results.dropna()
            results.sort_values(by=['Producto'],inplace=True)
            Listado.sort_values(by=['Producto'],inplace=True)
            results=results.reset_index(drop=True)
            Listado=results.reset_index(drop=True)
            if (results.equals(Listado))==True:
                print("Son iguales")
            else:
                print("WARNING")
                Listado.to_excel(r'PDF\Listado.xlsx')
                results.to_excel(r'PDF\results.xlsx')
                print(results)
    else:
        print("La tabla no existe, debemos crearla con el dataframe.")
        Listado.to_sql(name='stocks', con=conn, if_exists='replace', index=False)
    conn.commit()
