from django.urls import path
from sitio_personal import views
from django.contrib import admin


"""
URL patterns para la aplicación sitio_personal.

Este módulo define las rutas URL y las vistas correspondientes para la aplicación.
"""

urlpatterns = [
    path('', views.index, name='index'),
    path('blog/', views.blog, name='blog'),
    path('resume/', views.resume, name='resume'),
    path('about/', views.about, name='about'),
    path('admin/', admin.site.urls),
    path('articulos/', views.listar_articulos, name='listar_articulos'),
    path('contacto/', views.contact, name='contacto'),
    path('articulo/<int:articulo_id>/', views.detalle_articulo, name='detalle_articulo'),
    path('articulo/<int:article_id>/like/', views.like_article, name='like_article'),
    path('suscribirse/', views.suscribirse, name='suscribirse'),
    path('suscripcion-exitosa/', views.suscripcion_exitosa, name='suscripcion_exitosa'),
    
]
