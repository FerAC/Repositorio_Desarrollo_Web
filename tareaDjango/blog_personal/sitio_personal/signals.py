from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

from django.conf import settings
from .models import Articulo, Suscripcion

@receiver(post_save, sender=Articulo)
def enviar_notificacion_nuevo_articulo(sender, instance, created, **kwargs):
    """
    Función para enviar notificación de nuevo artículo.

    Esta función se activa cada vez que se guarda un nuevo artículo.
    Envía una notificación por correo electrónico a todas las suscripciones activas que desean recibir notificaciones.

    Parámetros:
        sender (class): La clase del remitente.
        instance (Articulo): La instancia del artículo que ha sido guardada.
        created (bool): Indica si la instancia es nueva o ya existente.

    Retorna:
        None
    """
    print("------------------------------------------ENTRA A SENAL")
    if created:
        # Obtener todas las suscripciones que deseen recibir notificaciones
        suscripciones = Suscripcion.objects.filter(recibir_notificaciones=True) 
        for suscripcion in suscripciones:
            enviar_correo_notificacion(suscripcion, instance)


def enviar_correo_notificacion(suscripcion, articulo):
    """
    Función para enviar correo de notificación de nuevo artículo.

    Envía un correo electrónico de notificación de nuevo artículo a una suscripción específica.

    Parámetros:
        suscripcion (Suscripcion): La suscripción a la cual enviar la notificación.
        articulo (Articulo): El artículo nuevo que ha sido publicado.

    Retorna:
        None
    """
    subject = 'Nuevo artículo en el blog'
    message = f'Hola {suscripcion.nombre},\n\nSe ha publicado un nuevo artículo en el blog:\n Titulo:\n{articulo.titulo}\n Preview: \n{articulo.preview}\n\nSaludos!'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [suscripcion.email]
    send_mail(subject, message, from_email, recipient_list)