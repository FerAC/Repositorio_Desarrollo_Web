from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Etiqueta(models.Model):
    """
    Clase que representa una etiqueta.

    Atributos:
        nombre (CharField): El nombre de la etiqueta.
    """
    nombre = models.CharField(max_length=100)

    def __str__(self):
        """
        Representación en cadena de la etiqueta.

        Retorna:
            str: El nombre de la etiqueta.
        """
        return self.nombre

class Articulo(models.Model):
    """
    Clase que representa un artículo.

    Atributos:
        titulo (CharField): El título del artículo.
        contenido (TextField): El contenido del artículo.
        etiquetas (ManyToManyField): Las etiquetas asociadas al artículo.
        fecha_publicacion (DateTimeField): La fecha y hora de publicación del artículo.
        likes (IntegerField): La cantidad de "me gusta" que tiene el artículo.
        thumbnail (ImageField): La imagen en miniatura del artículo.
        preview (TextField): Una vista previa del contenido del artículo.
        tiempo_lectura (IntegerField): El tiempo estimado de lectura del artículo en minutos.
    """
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    etiquetas = models.ManyToManyField(Etiqueta)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    thumbnail = models.ImageField(upload_to='sitio_personal/static/img/thumbnails', null=True, blank=True)
    preview = models.TextField(null=True, blank=True)
    tiempo_lectura = models.IntegerField(default=5)
    
    def thumbnail_name(self):
        """
        Obtiene el nombre de la imagen en miniatura.

        Retorna:
            str: El nombre del archivo de la imagen en miniatura, o None si no hay miniatura.
        """
        if self.thumbnail and self.thumbnail.name:
            return self.thumbnail.name.split('/')[-1]
        return None

    def __str__(self):
        """
        Representación en cadena del artículo.

        Retorna:
            str: El título del artículo.
        """
        return self.titulo
    
    def total_likes(self):
        return self.likes.count()
    
class Comentario(models.Model):
    articulo = models.ForeignKey(Articulo, related_name='comentarios', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    cuerpo = models.TextField()
    fecha = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Comentario de {self.nombre} en {self.articulo}'
