from django import forms
from .models import Evento

class FormularioContacto(forms.Form):
	nombre =forms.CharField(max_length=60)
	apellidos = forms.CharField(max_length=60)
	email = forms.EmailField(max_length=60)
	celular = forms.CharField(max_length=60)	
	mensaje = forms.CharField(widget=forms.Textarea)

class FormularioRegistro(forms.Form):
	nombre =forms.CharField(max_length=60)
	apellidos = forms.CharField(max_length=60)
	email = forms.EmailField(max_length=60)
	celular = forms.CharField(max_length=60)

class FormularioReserva(forms.Form):
	nombre =forms.CharField(max_length=60, required=True)
	apellidos = forms.CharField(max_length=60, required=True)
	celular = forms.CharField(max_length=60, required=True)
	email = forms.EmailField(max_length=60, required=True)
	numero_personas = forms.IntegerField(min_value=1, max_value=12, required=True)

class FormularioEmpleado(forms.Form):
	nombre = forms.CharField(max_length=60, required=True)
	email = forms.EmailField(max_length=60, required=True)
	mensaje = forms.CharField(widget=forms.Textarea)

class EventoForm(forms.ModelForm):
	model = Evento

	# class Meta:
	# 	widgets = {
 #            'descripcion': RedactorWidget(editor_options={'lang': 'en'})
 #            }

