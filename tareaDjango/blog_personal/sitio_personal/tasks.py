# sitio_personal/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Suscripcion, Articulo
from django.utils import timezone
from datetime import timedelta

@shared_task
def enviar_boletin_diario():
    print("IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")
    print("SE ENTRA A TASK")
    today = timezone.now().date()
    suscripciones = Suscripcion.objects.filter(frecuencia='diario')
    for suscripcion in suscripciones:
        articulos = Articulo.objects.filter(fecha_publicacion__date=today)
        if articulos.exists():
            enviar_boletin(suscripcion, articulos)

@shared_task
def enviar_boletin_mensual():
    last_month = timezone.now().date() - timedelta(days=30)
    suscripciones = Suscripcion.objects.filter(frecuencia='mensual')
    for suscripcion in suscripciones:
        articulos = Articulo.objects.filter(fecha_publicacion__date__gte=last_month)
        if articulos.exists():
            enviar_boletin(suscripcion, articulos)

def enviar_boletin(suscripcion, articulos):
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print("SE INTENTA ENVIAR BOLETIN")
    subject = 'Nuevos artículos en el blog'
    message = f'Hola {suscripcion.nombre},\n\nEstos son los nuevos artículos:\n'
    for articulo in articulos:
        message += f'\n{articulo.titulo}\n{articulo.preview}\n'
    message += '\nSaludos!'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [suscripcion.email]
    send_mail(subject, message, from_email, recipient_list)
