from django.urls import path
from sitio_personal import views
from django.contrib import admin

urlpatterns = [
    path('', views.index, name='index'),
    path('blog/', views.blog, name='blog'),
    path('resume/', views.resume, name='resume'),
    path('about/', views.about, name='about'),
    path('admin/', admin.site.urls),
    path('articulos/', views.listar_articulos, name='listar_articulos'),
]