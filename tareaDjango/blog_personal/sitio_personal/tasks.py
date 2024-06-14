from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Suscripcion, Articulo
from django.utils import timezone
from datetime import timedelta
from .models import Articulo, Comentario

class SitioPersonalConfig(AppConfig):
    name = 'sitio_personal'

    def ready(self):
        post_migrate.connect(create_groups_and_permissions, sender=self)

@receiver(post_migrate)
def create_groups_and_permissions(sender, **kwargs):
    admin_group, created = Group.objects.get_or_create(name='Administrador')
    subscriber_group, created = Group.objects.get_or_create(name='Suscriptor')
    moderator_group, created = Group.objects.get_or_create(name='Moderador')

    content_type_articulo = ContentType.objects.get_for_model(Articulo)
    content_type_comentario = ContentType.objects.get_for_model(Comentario)

    # Permisos para Administrador
    permisos_admin = Permission.objects.filter(content_type__in=[content_type_articulo, content_type_comentario])
    admin_group.permissions.set(permisos_admin)

    # Permisos para Suscriptor
    permisos_suscriptor = [
        Permission.objects.get(codename='add_comentario', content_type=content_type_comentario),
        Permission.objects.get(codename='change_comentario', content_type=content_type_comentario),
        Permission.objects.get(codename='delete_comentario', content_type=content_type_comentario),
        Permission.objects.get(codename='view_comentario', content_type=content_type_comentario),
        # Añade permisos para likes y dislikes si los tienes
    ]
    subscriber_group.permissions.set(permisos_suscriptor)

    # Permisos para Moderador
    permisos_moderador = [
        Permission.objects.get(codename='delete_comentario', content_type=content_type_comentario),
        Permission.objects.get(codename='change_comentario', content_type=content_type_comentario),
        Permission.objects.get(codename='view_comentario', content_type=content_type_comentario),
    ]
    moderator_group.permissions.set(permisos_moderador)
    
@shared_task
def enviar_boletin_diario():
    """
    Función que envía boletines diarios a las suscripciones activas.

    Obtiene la fecha actual y busca las suscripciones diarias en la base de datos.
    Si hay nuevos artículos publicados en el día, envía un boletín a cada suscripción.

    Parámetros:
        Ninguno.

    Retorna:
        Ninguno.
    """
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
    """
    Función que envía boletines mensuales a las suscripciones activas.

    Calcula la fecha del último mes y busca las suscripciones mensuales en la base de datos.
    Si hay nuevos artículos publicados en el último mes, envía un boletín a cada suscripción.

    Parámetros:
        Ninguno.

    Retorna:
        Ninguno.
    """
    last_month = timezone.now().date() - timedelta(days=30)
    suscripciones = Suscripcion.objects.filter(frecuencia='mensual')
    for suscripcion in suscripciones:
        articulos = Articulo.objects.filter(fecha_publicacion__date__gte=last_month)
        if articulos.exists():
            enviar_boletin(suscripcion, articulos)

def enviar_boletin(suscripcion, articulos):
    """
    Función que envía un boletín de nuevos artículos a una suscripción.

    Crea el mensaje del boletín con los títulos y vistas previas de los nuevos artículos.
    Envía el correo electrónico utilizando la configuración de correo de Django.

    Parámetros:
        suscripcion (Suscripcion): Objeto de suscripción.
        articulos (QuerySet): Conjunto de artículos nuevos.

    Retorna:
        Ninguno.
    """
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
