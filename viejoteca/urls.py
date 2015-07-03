"""viejoteca URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from website.views import *

urlpatterns = [
	url(r'^$', index),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^eventos/$', eventos, name='eventos'),	
	url(r'^eventos/proximos-eventos/(?P<pk>\d+)/$', pagina_evento_proximo, name='pagina_evento_proximo'),
	url(r'^eventos/historico-de-eventos/$', historico_eventos, name='historico_eventos'), 
	url(r'^eventos/historico-eventos/(\d+)/(\d+)/$', eventos_del_mes, name='eventos_del_mes'),
	url(r'^eventos/historico-de-eventos/(?P<year>\d+)/(?P<month>\d+)/(?P<nombre>[\w\-\W]+)/$', pagina_evento, name='pagina_evento'),
	url(r'^sobre-nosotros/', sobre_nosotros, name='sobre_nosotros'),
	url(r'^lista-de-precios/', lista_de_precios, name='lista-de-precios'), 
	url(r'^galeria/', galeria, name='galeria'), 
	url(r'^reservas/$', reservas, name='reservas'), 
	url(r'^contacto/$', contacto, name='contacto'),	
]
