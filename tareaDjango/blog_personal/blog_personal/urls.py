from django.urls import path
from sitio_personal import views

urlpatterns = [
    path('', views.index, name='index'),
    path('blog/', views.blog, name='blog'),
    path('resume/', views.resume, name='resume'),
    path('about/', views.about, name='about'),
]