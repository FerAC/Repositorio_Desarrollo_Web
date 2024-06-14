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
    """
    Clase que representa un comentario en un artículo.

    Atributos:
        articulo (ForeignKey): El artículo al que pertenece el comentario.
        nombre (CharField): El nombre del autor del comentario.
        cuerpo (TextField): El cuerpo del comentario.
        fecha (DateTimeField): La fecha y hora de publicación del comentario.
        parent (ForeignKey, opcional): El comentario al que responde este comentario (si es una respuesta).
        es_respuesta (BooleanField): Indica si el comentario es una respuesta a otro comentario.
    """
    articulo = models.ForeignKey(Articulo, related_name='comentarios', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    cuerpo = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='likes_coment', blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='respuestas', on_delete=models.CASCADE)
    es_respuesta = models.BooleanField(default=False)
    
    def total_likes(self):
        return self.likes.count()
    
    class Meta:
        ordering = ['-fecha']
        permissions = [
            ("highlight_comment", "Can highlight comment"),
        ]

    def __str__(self):
        """
        Representación en cadena del comentario.

        Retorna:
            str: Una cadena que representa el comentario.
        """
        return f'Comentario de {self.nombre} en {self.articulo}'

    def is_reply(self):
        """
        Verifica si el comentario es una respuesta.

        Retorna:
            bool: True si es una respuesta, False en caso contrario.
        """
        return self.parent is not None
    

class Suscripcion(models.Model):
    """
    Clase que representa una suscripción al blog.

    Atributos:
        email (EmailField): El correo electrónico de la suscripción.
        nombre (CharField): El nombre asociado a la suscripción.
        frecuencia (CharField): La frecuencia de interacción deseada (diario, semanal, mensual).
        recibir_notificaciones (BooleanField): Indica si la suscripción desea recibir notificaciones.
        fecha_suscripcion (DateTimeField): La fecha y hora en que se realizó la suscripción.
    """
    email = models.EmailField()
    nombre = models.CharField(max_length=100)
    frecuencia = models.CharField(max_length=10, choices=[('diario', 'Diario'), ('semanal', 'Semanal'), ('mensual', 'Mensual')])
    recibir_notificaciones = models.BooleanField(default=False)
    fecha_suscripcion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Representación en cadena de la suscripción.

        Retorna:
            str: Una cadena que representa la suscripción.
        """
        return f'{self.nombre} ({self.email})'
    
class MensajeContacto(models.Model):
    """
    Clase que representa un mensaje de contacto.

    Atributos:
        nombre (CharField): El nombre del remitente del mensaje.
        email (EmailField): El correo electrónico del remitente del mensaje.
        cuerpo (TextField): El cuerpo del mensaje de contacto.
        fecha_envio (DateTimeField): La fecha y hora en que se envió el mensaje.
    """
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    cuerpo = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Mensaje de {self.nombre} ({self.email})'

