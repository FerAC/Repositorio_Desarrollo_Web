from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

from django.conf import settings
from .models import Articulo, Suscripcion

@receiver(post_save, sender=Articulo)
def enviar_notificacion_nuevo_articulo(sender, instance, created, **kwargs):
    print("------------------------------------------ENTRA A SENAL")
    if created:
        # Obtener todas las suscripciones que deseen recibir notificaciones
        suscripciones = Suscripcion.objects.filter(recibir_notificaciones=True)
        for suscripcion in suscripciones:
            enviar_correo_notificacion(suscripcion, instance)


def enviar_correo_notificacion(suscripcion, articulo):
    subject = 'Nuevo artículo en el blog'
    message = f'Hola {suscripcion.nombre},\n\nSe ha publicado un nuevo artículo en el blog:\n\n{articulo.titulo}\n{articulo.preview}\n\nSaludos!'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [suscripcion.email]
    send_mail(subject, message, from_email, recipient_list)