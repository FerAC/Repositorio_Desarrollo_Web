from django.db import models

class Etiqueta(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Articulo(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    etiquetas = models.ManyToManyField(Etiqueta)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    thumbnail = models.ImageField(upload_to='sitio_personal/static/img/thumbnails', null=True, blank=True)
    preview = models.TextField(null=True, blank=True)
    tiempo_lectura = models.IntegerField(default=5)
    
    def thumbnail_name(self):
        if self.thumbnail and self.thumbnail.name:
            return self.thumbnail.name.split('/')[-1]
        return None

    def __str__(self):
        return self.titulo;
