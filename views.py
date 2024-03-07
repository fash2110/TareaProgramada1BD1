from re import template
from unittest import loader
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from .models import Sistema
from .forms import FormularioInsertar
import pyodbc





# Create your views here.
def sistema(request):
    conn = pyodbc.connect('DSN=DSN_P1;UID=PySQL;PWD=1234')

    cursor = conn.cursor()
    mymembers = []

    cursor.execute("EXEC ListarEmpleados")
    #print(cursor.description[0][0])
    columns = [column[0] for column in cursor.description]
    for row in cursor.fetchall():
        #print(dict(zip(columns, row))['id'], dict(zip(columns, row))['Nombre'], dict(zip(columns, row))['Salario'])
        mymembers = mymembers + [ (dict(zip(columns, row))['id'], dict(zip(columns, row))['Nombre'], float(dict(zip(columns, row))['Salario'])) ]

    template = loader.get_template('all_members.html')
    context = {'mymembers': mymembers,}
    conn.close()
    return HttpResponse(template.render(context, request))

def insertar(request):
    conn = pyodbc.connect('DSN=DSN_P1;UID=PySQL;PWD=1234')

    cursor = conn.cursor()
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = FormularioInsertar(request.POST)
        # check whether it's valid:
        print(form.is_valid())
        if form.is_valid():
            # process the data in form.cleaned_data as required
            print("EXEC InsertarEmpleado " + form.cleaned_data['eNombre'] + " " + str(form.cleaned_data['eSalario']))
            conn.execute("EXEC InsertarEmpleado '" + form.cleaned_data['eNombre'] + "', " + str(form.cleaned_data['eSalario']))
            # redirect to a new URL:
            return HttpResponseRedirect("/thanks/")
        print('no')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = FormularioInsertar()
    conn.close()
    return render(request, "insertar.html", {"form": form})


def thanks(request):
    conn = pyodbc.connect('DSN=DSN_P1;UID=PySQL;PWD=1234')

    cursor = conn.cursor()
    template = loader.get_template('thanks.html')
    conn.close()
    return HttpResponse(template.render())
