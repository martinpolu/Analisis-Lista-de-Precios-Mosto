import sqlite3
import pathlib
import plotly.express as px
import pandas as pd



RelativePath=str(pathlib.Path(__file__).parent.resolve())
con = sqlite3.connect(RelativePath+"/PDF/ListaDePrecios.db") #Buscamos el .db
def sql_fetch(con):
    Columnas=[]
    cursor=con.execute('''SELECT * FROM stocks''') #Query para identificar columnas de .db
    ColumBuff = cursor.description[1:]
    for column in ColumBuff:
        Columnas.append(column[0])
    print("Que desea realizar:"+"\n"+"A) Últimas dos listas de precios"+"\n"+"B) Elegir dos listas de precios")
    Opc0 = input().upper()
    while(Opc0!='A' and Opc0!='B'):
        print("Por favor reingrese una opción correcta")
        Opc0 = input().upper()
        print(Opc0)
    if(Opc0=='B'):
            for f,column in enumerate(Columnas):
                print(str(f)+"--->"+str(column))
            Opc1 = int(input())
            Opc2 = int(input())
    else:
        Opc1 = len(Columnas)-2
        Opc2 = len(Columnas)-1
    print(Columnas[Opc1])
    print(Columnas[Opc2])
    query=str("Producto"+',"'+Columnas[Opc1]+'","'+Columnas[Opc2]+'"') #Generamos el query para seleccionar solo las dos ultimas
    cursor=con.execute('SELECT ' + query+ ' FROM stocks')
    rows = cursor.fetchall()
    df=(pd.DataFrame(rows))
    df.columns=["Producto",Columnas[Opc1],Columnas[Opc2]]
    df.set_index("Producto",inplace=True)
    df = df.sort_values('Producto')
    df.dropna(subset=[Columnas[Opc2], Columnas[Opc1]], how='all', inplace=True)
    df=df[(df != 0).all(1)]
    df = df[df[Columnas[Opc2]] != df[Columnas[Opc1]]]
    df.to_excel(r'PDF\output1.xlsx')
sql_fetch(con)
