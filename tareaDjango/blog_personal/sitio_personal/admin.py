from django.contrib import admin
from .models import Articulo
from .models import Etiqueta

admin.site.register(Articulo)
admin.site.register(Etiqueta)