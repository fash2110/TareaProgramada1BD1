from re import template
from unittest import loader
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from .models import Sistema
from .forms import FormularioInsertar
import pyodbc
import re

# Create your views here.
def sistema(request):
    conn = pyodbc.connect('DSN=DSN_P1;UID=PySQL;PWD=1234', autocommit=True)
    cursor = conn.cursor()
    mymembers = []
    cursor.execute("EXEC ListarEmpleados")
    
    #print(cursor.description[0][0])
    columns = [column[0] for column in cursor.description]
    for row in cursor.fetchall():
        mymembers = mymembers + [ (dict(zip(columns, row))['id'], dict(zip(columns, row))['Nombre'], float(dict(zip(columns, row))['Salario'])) ]

    template = loader.get_template('all_members.html')
    context = {'mymembers': mymembers,}
    cursor.close()
    conn.close()
    return HttpResponse(template.render(context, request))

def insertarUsuario(form):
    '''
    Funcionamiento: Ejecuta la sentencia SQL para insertar un empleado con los datos del formulario
    Entrada: datos del empleado [form]
    Salida:
        -True: El empleado se ingresó con éxito
        -False: Hubo un error en la inserción
    '''
    conn = pyodbc.connect('DSN=DSN_P1;UID=PySQL;PWD=1234', autocommit=True)
    cursor = conn.cursor()
    try:
        statement = """\
                    SET NOCOUNT ON;
                    DECLARE @out INT;
                    EXEC [dbo].[InsertarEmpleado] @inNombre = ?, @inSalario = ?, @outResultCode = @out OUTPUT;
                    SELECT @out AS the_output;
                    """
        cursor.execute(statement, (form.cleaned_data['eNombre'], form.cleaned_data['eSalario'], ))
        for result in cursor.fetchall():
            if result[0] == 0:  #resultado = 0, no hay errores
                conn.commit()
                return True
            else:
                return False
    except Exception as e:
        print("An error occurred:", e)
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

def validarInsercion(formulario):
    '''
    Funcionamiento: Valida que los datos del formulario sean correctos
    Entrada: datos del empleado [form]
    Salida:
        -True: No hay errores con los datos
        -False: Existe un error en los datos
    '''
    valido = True
    if not re.match(r"(^[a-zA-Z \-]+$)", formulario.cleaned_data['eNombre']): #Nombre con letras mayusculas, minusculas y guión
        print("nombre invalido")
        valido = False
    if not formulario.cleaned_data['eSalario'] >= 0.0: #Salario positivo
        print("Salario invalido")
        valido = False
    return valido
    

def insertar(request):
    if request.method == "POST": # if this is a POST request we need to process the form data
        form = FormularioInsertar(request.POST)
        if form.is_valid(): #Validaciones creadas por django (ambos campos están llenos, y el salario es un valor numerico)
            if validarInsercion(form):  #Validaciones personalizadas (Empleado son letras o guión, salario es positivo)
                if insertarUsuario(form):
                    return HttpResponseRedirect("/thanks/") #Confirmación que el empleado se insertó
                else:
                    return HttpResponseRedirect("/error/") #Error en caso que el empleado sea repetido o algún error micelaneo
            else:
                return HttpResponseRedirect("/error/") #Error en caso que los valores no sean validos
    else: # La primera vez que se entra a la página es con método GET, este else nos redirige con POST
        form = FormularioInsertar()
    return render(request, "insertar.html", {"form": form})

def thanks(request):
    template = loader.get_template('thanks.html')
    return HttpResponse(template.render())

def error(request):
    template = loader.get_template('error.html')
    return HttpResponse(template.render())