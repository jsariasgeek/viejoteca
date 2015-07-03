# -*- coding: utf-8 -*-

from django.shortcuts import render

from django.template import loader, Context
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response, get_object_or_404
from django.db import transaction
from website.models import *
from website.forms import *
from django.views.decorators.cache import never_cache
from django.core.context_processors import csrf
from django.template import RequestContext
from django.core.mail import EmailMessage
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

months_name = {
	1:'Enero',
	2:'Febrero',
	3:'Marzo',
	4:'Abril',
	5:'Mayo',
	6:'Junio',
	7:'Julio',
	8:'Agosto',
	9:'Septiembre',
	10:'Octubre',
	11:'Noviembre',
	12:'Diciembre'
}


def index(request):
	eventos_slide = Evento.objects.filter(fecha__gte=timezone.now()).order_by('fecha')[:5]	
	galeria_slide = ImagenGallery.objects.order_by('-fecha_subida')[:5]
	return render_to_response("index.html", dict(eventos_proximos = eventos_slide, galeria_slide=galeria_slide, form=FormularioRegistro()), context_instance=RequestContext(request))

def eventos(request):	
	evento_inminente = Evento.objects.filter(fecha__gte=timezone.now()).order_by('fecha')[0]
	month_inminente = months_name[evento_inminente.fecha.month]
	eventos_proximos = Evento.objects.filter(fecha__gte=timezone.now()).order_by('fecha')[1:]
	eventos_pasados = Evento.objects.exclude(fecha__gte=timezone.now()).order_by('-fecha')[:12]
	return render_to_response('eventos.html', dict(evento_inminente=evento_inminente, eventos_proximos=eventos_proximos, eventos_pasados=eventos_pasados, month_inminente=month_inminente, form=FormularioReserva()), context_instance=RequestContext(request))
# 	#Algoritmo que tiene que realizar la consulta:
# 	#Extraer solo los eventos proximos
# 	#De los eventos proximos traer el más proximo:Debe restarle a la fecha del evento 
# 	#la fecha actual y almacenarlo en una variable llamada diferencia. Posteriormente, debe de retornar
# 	#el evento con menor diferencia posible.
# 	eventoProximo = Evento.objects.filter(self.fecha.date() > timezone.now.date())	
# 	return render_to_response('eventos.html', dict(eventoProximo = eventoProximo))

def historico_eventos(request):	
	date = Evento.objects.dates('fecha', 'month', order='DESC').exclude(fecha__gte=timezone.now())[0] 
	month_actual = months_name[date.month]
	eventos_pasados = Evento.objects.exclude(fecha__gte=timezone.now()).order_by('-fecha')
	eventos_del_mes =  Evento.objects.filter(fecha__month=date.month, fecha__year=date.year).exclude(fecha__gte=timezone.now())
	arch = Evento.objects.dates('fecha', 'month', order='DESC').exclude(fecha__gte=timezone.now()) 
	archives = {} 	
	for i in arch:
		tp = i.timetuple()
		year = tp[0]
		month = tp[1]	

		if year not in archives:
			archives[year] = []
			archives[year].append(month)
		else:
			if month not in archives[year]:
				archives[year].append(month)

	pagination = sorted(archives.items(), reverse=True)

	for i in pagination:
		year = i[0]
		months = i[1]	

	return render_to_response('historico-eventos.html', dict(eventos_pasados = eventos_pasados, date=date, month_actual=month_actual, eventos_del_mes=eventos_del_mes, pagination=pagination ))
	

def sobre_nosotros(request, pk=None):
	form = FormularioEmpleado(request.POST or None)
	empleados = Empleado.objects.all()
	# contenido_sitio = ContenidoSitioWeb.objects.all()

	if form.is_valid():
			try:
				EmpleadoMensaje = MensajeEmpleado()
				EmpleadoMensaje.empleado = Empleado.objects.get(pk=pk)
				EmpleadoMensaje.mensaje = form.cleaned_data['mensaje']
				EmpleadoMensaje.suscriptor = Suscriptor.objects.get(email=form.cleaned_data['email'])
				EmpleadoMensaje.save()
				return HttpResponse('Tu mensaje se ha enviado correctamente')
			except ObjectDoesNotExist:
				return HttpResponse('Para enviar el mensaje debes ser usuario registrado <br> <a class="btn btn-default" href="#">REGISTRARME<a>')
	
	return render_to_response('sobre-nosotros.html', dict(empleados = empleados, form=form,), context_instance=RequestContext(request))

def carta(request):
	return render_to_response('carta.html') 

def contacto(request):
	form = FormularioContacto(request.POST or None)

	if form.is_valid(): # Si es válido se procesan los datos
			nombres = form.cleaned_data['nombre']
			apellidos = form.cleaned_data['apellidos']
			email = form.cleaned_data['email']
			celular = form.cleaned_data['celular']
			mensajeUsuario = form.cleaned_data['mensaje']					
			subject = 'Te han dejado un mensaje en la web'
			message = nombres + ' ' + apellidos + ' con el email ' + email + ' y celular ' + celular + ' te ha dejado el siguiente mensaje en la web:  ' + mensajeUsuario
			# Enviamos el mensaje
			mail = EmailMessage(subject, message, to=['voipereira@gmail.com', 'jsarias1993@gmail.com'])
			mail.send()

			# Guardamos los datos del usuario
			userMessage = Suscriptor()
			userMessage.nombres = form.cleaned_data['nombre']
			userMessage.apellidos = form.cleaned_data['apellidos']
			userMessage.email = form.cleaned_data['email']
			userMessage.celular = form.cleaned_data['celular']

			
			# Guardamos el Mensaje

			# Guardamos el usuario
			try:
				userMessage.save()
				userMessage.mensaje_set.create(mensaje=mensajeUsuario)
				return HttpResponse('Tu mensaje se ha enviado Correctamente')

			except IntegrityError:
				# confirmamos el envío del mensaje			
				UserHistorico = Suscriptor.objects.get(email=email)
				messageUser = Mensaje()
				messageUser.usuario = UserHistorico
				messageUser.mensaje = mensajeUsuario
				messageUser.save()
				return HttpResponse('Tu mensaje se ha enviado Correctamente. <br> Pronto te Contactaremos')
	return render_to_response('contacto.html', dict(form=FormularioContacto()), context_instance=RequestContext(request))




def registro(request):
	if request.method == 'POST': # Si el formulario es enviado
		form = FormularioRegistro(request.POST)		
		if form.is_valid(): # Si es válido se procesan los datos
			nombres = form.cleaned_data['nombre']
			apellidos = form.cleaned_data['apellidos']
			email = form.cleaned_data['email']
			celular = form.cleaned_data['celular']			

			# Guardamos los datos del usuario
			userMessage = Suscriptor()
			userMessage.nombres = form.cleaned_data['nombre']
			userMessage.apellidos = form.cleaned_data['apellidos']
			userMessage.email = form.cleaned_data['email']
			userMessage.celular = form.cleaned_data['celular']		
			

			# Guardamos el usuario
			try:
				userMessage.save()				
				return HttpResponse('Bienvenido al Club Social La Viejoteca de la quinta. Te has REgistrado Exitosamente.')

			except IntegrityError:		
				return HttpResponse('Usted ya se encuentra registrado en nuestra base de datos.')
			
	else:
		form = FormularioContacto() # An unbound form

	return render_to_response('index.html', dict(form=form), context_instance=RequestContext(request))






def eventos_del_mes(request, year, month):		
	month_requerido = months_name[int(month)]	
	eventos_del_mes = Evento.objects.filter(fecha__year=year, fecha__month=month).exclude(fecha__gte=timezone.now())
	return render_to_response('eventosdelmes.html', dict(eventos_del_mes=eventos_del_mes, year=year, month=month_requerido, usuario=request.user))


def pagina_evento(request, year, month, nombre):	
	eventos_del_mes = Evento.objects.filter(fecha__year=year, fecha__month=month)
	for evento in eventos_del_mes:
		if evento.get_absolute_url() == nombre:
			evento_buscado = evento
			break

	eventos_relacionados = eventos_del_mes.exclude(pk=evento_buscado.pk).exclude(fecha__gte=timezone.now())
	# import ipdb; ipdb.set_trace()
	return render_to_response('fotos-evento.html', dict(evento=evento_buscado, eventos_relacionados=eventos_relacionados))


def lista_de_precios(request):
	return render_to_response('lista-de-precios.html')

@never_cache
def galeria(request):
	imagenGallery = ImagenGallery.objects.all().order_by('-fecha_subida')
	videos = Video.objects.all().order_by('-fecha')

	return render_to_response('galeria.html', dict(imagenes = imagenGallery, videos=videos))

def not_found(request):
	return render_to_response('404.html')

# def reservas(request):
# 	if request.method == 'POST':
# 		form = FormularioReserva(request.POST)
# 		if form.is_valid():
# 			nombre = form.cleaned_data['nombre']
# 			apellidos = form.cleaned_data['apellidos']
# 			celular = form.cleaned_data['celular']
# 			email = form.cleaned_data['email']
# 			numero_personas = form.cleaned_data['numero_personas']
# 			evento = Evento.objects.get(pk=pk)
# 			success = 'La Reserva se ha hecho satisfactoriamente. Por favor Revisa tu Correo para ver las instrucciones.'


# 			# Guardamos los datos del usuario
# 			userReserva = Suscriptor()
# 			userReserva.nombres = form.cleaned_data['nombre']
# 			userReserva.apellidos = form.cleaned_data['apellidos']
# 			userReserva.email = form.cleaned_data['email']
# 			userReserva.celular = form.cleaned_data['celular']

# 			strEvento = str(evento)
# 			subject = 'Se ha solicitado una reserva para el evento ' + strEvento
# 			message = nombre + ' ' + apellidos + ' con el email ' + email + ' y celular ' + celular + ' ha solicitado una reserva para el evento ' + strEvento + '. Numero de Personas: ' + str(numero_personas)
# 			# Enviamos el mensaje
# 			mail = EmailMessage(subject, message, to=['voipereira@gmail.com'])
# 			mail.send()

# 			# subject = 'Se ha solicitado una reserva para el evento ' + evento
# 			# message = nombre + ' ' + apellidos + ' con el email ' + email + ' y celular ' + celular + 'ha solicitado una reserva para el evento ' + evento + '. Numero de Personas: ' + numero_personas
# 			# # Enviamos el mensaje
# 			# mail = EmailMessage(subject, message, to=['jsarias1993@gmail.com'])
# 			# mail.send()



# 			# Guardamos el usuario
# 			try:
# 				userReserva.save()
# 				userReserva.reserva_set.create(evento=evento, numero_personas=numero_personas, numero_mesas=int(numero_personas)/4)
# 				return HttpResponse(success)

# 			except IntegrityError:
# 				# confirmamos el envío del mensaje			
# 				UserHistorico = Suscriptor.objects.get(email=email)				
# 				reservaUser = Reserva()
# 				reservaUser.suscriptor = UserHistorico
# 				reservaUser.evento = evento
# 				reservaUser.numero_personas = numero_personas	
# 				reservaUser.numero_mesas = int(numero_personas)/4			
# 				reservaUser.save()
# 				return HttpResponse(success)
			
# 	else:
# 		form = FormularioReserva() # An unbound form
# 		return render_to_response('eventos.html', dict(form=form), context_instance=RequestContext(request))

def reservas(request):
	return render_to_response('reservas.html')
			
def pagina_evento_proximo(request, pk):	
	evento = Evento.objects.get(pk=pk)	
	videos_artista = VideosArtista.objects.filter(evento=evento)[:2]
	len_videos = len(videos_artista)
	return render_to_response('pagina-evento-proximo.html', dict(evento=evento, videos_artista=videos_artista, len_videos=len_videos))
			
			