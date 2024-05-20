from django.contrib import admin
from .models import Articulo
from .models import Etiqueta
from .models import Comentario

class ComentarioInline(admin.TabularInline):
    model = Comentario
    extra = 1
    fk_name = 'parent'

class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'articulo', 'fecha', 'parent')
    list_filter = ('fecha', 'articulo')
    search_fields = ('nombre', 'cuerpo')
    inlines = [ComentarioInline]

admin.site.register(Articulo)
admin.site.register(Comentario, ComentarioAdmin)
admin.site.register(Etiqueta)