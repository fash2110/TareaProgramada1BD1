from django import forms

class FormularioInsertar(forms.Form):
    eNombre = forms.CharField(label="Nombre", max_length=100, strip=True, required=True)
    eSalario = forms.DecimalField(label="Salario", max_digits=32, required=True)
