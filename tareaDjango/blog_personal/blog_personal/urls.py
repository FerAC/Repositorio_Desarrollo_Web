from django.urls import path
from sitio_personal import views
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect


"""
URL patterns para la aplicación sitio_personal.

Este módulo define las rutas URL y las vistas correspondientes para la aplicación.
"""

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/', include('allauth.urls')),
    path('accounts/login/', lambda request: redirect('socialaccount_login', 'google')),
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
    path('comentario/<int:comentario_id>/eliminar/', views.eliminar_comentario, name='eliminar_comentario'),
    path('comentario/<int:comentario_id>/like/', views.like_comentario, name='like_comentario'),

]
