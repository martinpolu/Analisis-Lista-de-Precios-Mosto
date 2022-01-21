import sqlite3
import pathlib
import plotly.express as px
import pandas as pd





RelativePath=str(pathlib.Path(__file__).parent.resolve())
Seleccion='"TRAPICHE RESERVA MALBEC X 750"'
con = sqlite3.connect(RelativePath+"/PDF/ListaDePrecios.db")
def sql_fetch(con):
    Precios=[]
    Columnas=[]
    cursorObj = con.cursor()
    cursorObj.execute('''SELECT * FROM stocks where Producto='''+str(Seleccion))
    rows = cursorObj.fetchall()
    for row in rows:
        Precios.append(row)
    Precios=Precios[0][1:]
    Precios=list(Precios)
    Base=Precios[0]
    Precios = [element / Base for element in Precios]
    cursor=con.execute('''SELECT * FROM stocks''')
    for column in cursor.description:
        Columnas.append(column[0])
    Columnas=Columnas[1:]
    df = pd.DataFrame(dict(
        Precio = Precios,
        Fecha = Columnas
    ))
    for i,j in zip(Precios,Columnas):
        print(i,j)
    fig = px.line(df, x= "Fecha",y="Precio", title='Evolución del precio.')
    fig.show()
sql_fetch(con)
