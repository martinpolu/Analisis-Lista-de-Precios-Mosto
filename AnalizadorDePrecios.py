import sqlite3
import pathlib
RelativePath=str(pathlib.Path(__file__).parent.resolve())

con = sqlite3.connect(RelativePath+"/PDF/ListaDePrecios.db")
def sql_fetch(con):
    Precios=[]
    Columnas=[]
    cursorObj = con.cursor()
    cursorObj.execute('''SELECT * FROM stocks where Producto="a"''')
    rows = cursorObj.fetchall()
    for row in rows:
        Precios.append(row)
    Precios=Precios[0][1:]
    print(Precios)
    cursor=con.execute('''SELECT * FROM stocks''')
    for column in cursor.description:
        Columnas.append(column[0])
    Columnas=Columnas[1:]
    for i,j in zip(Precios,Columnas):
        print(i,j)
sql_fetch(con)
