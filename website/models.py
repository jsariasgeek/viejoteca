# -*- coding: utf-8 -*-


from django.db import models

from django.db import models
from django.template.defaultfilters import slugify
# Create your models here.

#encoding:utf-8
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


# Create your models here.
 

class Suscriptor(models.Model):
	nombres = models.CharField(max_length=60)
	apellidos = models.CharField(max_length=60)
	email = models.EmailField(max_length=60, unique=True)
	celular = models.CharField(max_length=10)
	fecha_registro = models.DateTimeField(auto_now_add=True)	
	recibe_emails = models.BooleanField("Recibe Emails", default=True)
	recibe_sms = models.BooleanField("Recibe SMS", default=True)
	activo = models.BooleanField("Recibe Emails", default=False)

	def __str__(self):
		return (self.nombres + ' ' + self.apellidos)

	class Meta():
		verbose_name_plural = 'Suscriptores'

class ContactosdeApoyo(models.Model):
	nombres = models.CharField(max_length=60)
	telefono = models.CharField(max_length=10)
	id_user = models.ForeignKey(Suscriptor)
	fecha_creacion = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.nombres

class Mensaje(models.Model):
	usuario = models.ForeignKey(Suscriptor)
	mensaje = models.TextField()
	fecha_envio = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.mensaje[:60]

	class Meta():
		verbose_name = 'Mensaje de Usuario'
		verbose_name_plural = 'Mensajes de Usuarios'



class Evento(models.Model):
	nombre = models.CharField(max_length=120)
	# descripcion = HTMLField(help_text='Información adicional sobre el evento', blank=True)
	flyer = models.ImageField(upload_to='flyers',help_text='Recuerda que el flyer debe de tener las siguientes dimensiones: 1000px x 450px')
	flyer_thumbnail = ImageSpecField(source='flyer',
                                      processors=[ResizeToFill(640, 306)],
                                      format='JPEG',
                                      options={'quality': 80})
	flyer_thumbnail_historico = ImageSpecField(source='flyer',
                                      processors=[ResizeToFill(260, 124)],
                                      format='JPEG',
                                      options={'quality': 100})
	flyer_thumbnail_inminente = ImageSpecField(source='flyer',
                                      processors=[ResizeToFill(810, 365)],
                                      format='JPEG',
                                      options={'quality': 100})
	flyer_thumbnail_inminente_modal = ImageSpecField(source='flyer',
                                     processors=[ResizeToFill(1000, 450)],
                                      format='JPEG',
    
                                      options={'quality': 100})
	fecha = models.DateField()	
	src_album = models.URLField(blank=True)
	# url = models.SlugField(default=slugify(nombre))
	cuna_radial = models.URLField(blank=True)
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	fecha_actualizacion = models.DateTimeField(auto_now=True)
	

	def __str__(self):
		return self.nombre

	class Meta:
		ordering = ['-fecha']

	def get_absolute_url(self):
		return '%s' %(slugify(self.nombre))

	def save(self, *args, **kwargs):
		self.url = slugify(self.nombre)
		super (Evento, self).save(*args, **kwargs)

class VideosArtista(models.Model):
	evento = models.ForeignKey(Evento)
	url = models.URLField()

	def __str__(self):
		return self.url


class Reserva(models.Model):
	suscriptor = models.ForeignKey(Suscriptor)
	evento = models.ForeignKey(Evento)
	numero_personas = models.SmallIntegerField()
	numero_mesas = models.SmallIntegerField()
	fecha_reserva = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.suscriptor)

	class Meta():
		verbose_name_plural = 'Reservas'

class ImagenGallery(models.Model):
	Numero_Imagen = models.AutoField(primary_key=True)
	imagen = models.ImageField(upload_to='slides-home')
	fecha_subida = models.DateTimeField(auto_now_add=True)
	imagen_thumbnail = ImageSpecField(source='imagen',
                                      processors=[ResizeToFill(640, 306)],
                                      format='JPEG',
                                      options={'quality': 90})
	thumbnail_foto = ImageSpecField(source='imagen',
                                      processors=[ResizeToFill(300, 300)],
                                      format='JPEG',
                                      options={'quality': 100})

	def __str__(self):
		return str(self.Numero_Imagen)

	class Meta():
		verbose_name = 'Imagen'
		verbose_name_plural = 'Imagenes - Galería'

	def thumbnail_admin(self):
		return """
		<img src='%s' alt=''>
		"""% self.thumbnail_foto.url

	thumbnail_admin.allow_tags = True

class Empleado(models.Model):
	nombres = models.CharField(max_length=120)
	cargo = models.CharField(max_length=50)
	email = models.EmailField()
	foto = models.ImageField(upload_to='empleados', help_text='Recuerda que las fotos deben de ser cuadradas')
	foto_thumbnail = ImageSpecField(source='foto',
                                      processors=[ResizeToFill(248, 248)],
                                      format='JPEG',
                                      options={'quality': 100})
	foto_thumbnail_admin = ImageSpecField(source='foto',
                                      processors=[ResizeToFill(100, 100)],
                                      format='JPEG',
                                      options={'quality': 100})

	def __str__(self):
		return self.nombres

	def showfoto(self):
		return """
		<img src="%s" alt="">
		"""% self.foto_thumbnail_admin.url

	showfoto.short_description = 'Foto'
	showfoto.allow_tags = True

class MensajeEmpleado(models.Model):
	empleado = models.ForeignKey(Empleado)
	mensaje = models.TextField(max_length=240)
	fecha_envio = models.DateTimeField(auto_now_add=True)
	suscriptor = models.ForeignKey(Suscriptor)


	def __str__(self):
		return str(self.empleado)

	class Meta():
		verbose_name_plural = 'Mensajes a Empleados'

class Video(models.Model):
	titulo = models.CharField(max_length=60)
	fecha = models.DateField()
	url = models.URLField()

	def __str__(self):
		return self.titulo

# class ContenidoSitioWeb(models.Model):
# 	quienes_somos =  HTMLField(max_length=600)	

# 	def __str__(self):
# 		return ('Sección Quienes Somos')

# 	class Meta():
# 		verbose_name_plural = 'Contenido del Sitio Web'
		



