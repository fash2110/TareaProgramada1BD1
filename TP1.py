import pyodbc



conn = pyodbc.connect('DSN=DSN_P1;UID=PySQL;PWD=1234')

cursor = conn.cursor()

cursor.execute("EXEC ListarEmpleados")
print(cursor.description[0][0])
columns = [column[0] for column in cursor.description]
results = []
for row in cursor.fetchall():
    print(dict(zip(columns, row))['Nombre'])

    