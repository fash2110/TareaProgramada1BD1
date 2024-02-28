from unittest import loader
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Sistema
import pyodbc


conn = pyodbc.connect('DSN=DSN_P1;UID=PySQL;PWD=1234')

cursor = conn.cursor()



# Create your views here.
def sistema(request):
    mymembers = []

    cursor.execute("EXEC ListarEmpleados")
    #print(cursor.description[0][0])
    columns = [column[0] for column in cursor.description]
    for row in cursor.fetchall():
        #print(dict(zip(columns, row))['id'], dict(zip(columns, row))['Nombre'], dict(zip(columns, row))['Salario'])
        mymembers = mymembers + [ (dict(zip(columns, row))['id'], dict(zip(columns, row))['Nombre'], float(dict(zip(columns, row))['Salario'])) ]

    template = loader.get_template('all_members.html')
    context = {'mymembers': mymembers,}
    return HttpResponse(template.render(context, request))

def insertar(request):
    template = loader.get_template('insertar.html')
    return HttpResponse(template.render())