# -*- coding: utf-8 -*-


from django.contrib import admin
from website.models import Evento, VideosArtista, Empleado, ImagenGallery, Video, Reserva, Suscriptor, MensajeEmpleado, Mensaje
from .forms import EventoForm

class VideosArtistaInline(admin.StackedInline):
	model = VideosArtista
	extra = 0

class ReservaInline(admin.TabularInline):
    model = Reserva
    extra = 0

class EventoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha')
    # fieldsets = (
    #     [None,{'fields': ['nombre']}],
    #     ['Redactar Descripción', {
    #         'classes': ('full-width',),
    #         'fields': ('descripcion',)
    #     }],
    #     # [None,{'fields': ['descripcion',]}],    
    #     [None, {'fields': ['fecha'],}],
    #     [None, {'fields': ['flyer'],}],
    #     [None, {'fields': ['cuna_radial'],}],
    #     [None, {'fields': ['src_album'],}], 
    # )

    # form = EventoForm

    inlines = [VideosArtistaInline, ReservaInline]
    search_fields = ('nombre', 'id')


class MensajeEmpleadoAdmin(admin.ModelAdmin):
    list_display = ('empleado', 'mensaje', 'fecha_envio', 'suscriptor')


class ReservaAdmin(admin.ModelAdmin):
    list_display = ('suscriptor', 'evento', 'numero_personas','numero_mesas')   
    fieldsets = [
        (None, {'fields': ['suscriptor']}),
        (None, {'fields': ['evento']}),
        (None, {'fields': ['numero_personas']}),
    ]

class MensajeInline(admin.StackedInline):
    model = Mensaje
    extra = 0


class SuscriptorAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'apellidos', 'email', 'celular', 'fecha_registro', 'activo')
    inlines = [MensajeInline]

class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'showfoto','cargo', 'email')
    fieldsets = [
        (None,{'fields': ['nombres']}),
        (None,{'fields': ['cargo']}),    
        (None, {'fields': ['email'],}),
        (None, {'fields': ['foto'],}),      
                             
    ]



class MensajeAdmin(admin.ModelAdmin):
    list_display = ('mensaje', 'usuario', 'fecha_envio')

class ImagenGalleryAdmin(admin.ModelAdmin):
    list_display = ('thumbnail_admin',)

admin.site.register(Evento, EventoAdmin)
admin.site.register(Reserva, ReservaAdmin)
admin.site.register(Suscriptor, SuscriptorAdmin)
admin.site.register(Empleado, EmpleadoAdmin)
admin.site.register(MensajeEmpleado, MensajeEmpleadoAdmin)
admin.site.register(ImagenGallery, ImagenGalleryAdmin)
admin.site.register(Video)
admin.site.register(Mensaje, MensajeAdmin)


# class EventoAdmin(admin.ModelAdmin):
# 	list_display = ('nombre', 'fecha')


# admin.site.register(Evento, EventoAdmin)
# admin.site.register(VideosArtista)
