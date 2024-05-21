from django.contrib import admin
from .models import Articulo
from .models import Etiqueta
from .models import Comentario
from .models import MensajeContacto
from .models import Suscripcion
from django_celery_beat.models import PeriodicTask

class ComentarioInline(admin.TabularInline):
    model = Comentario
    extra = 1
    fk_name = 'parent'

class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'articulo', 'fecha', 'parent')
    list_filter = ('fecha', 'articulo')
    search_fields = ('nombre', 'cuerpo')
    inlines = [ComentarioInline]

class MensajeContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'fecha_envio')
    search_fields = ('nombre', 'email')

class SuscripcionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'frecuencia', 'fecha_suscripcion')

admin.site.register(Articulo)
admin.site.register(Comentario, ComentarioAdmin)
admin.site.register(Etiqueta)
admin.site.register(MensajeContacto)
admin.site.register(Suscripcion, SuscripcionAdmin)