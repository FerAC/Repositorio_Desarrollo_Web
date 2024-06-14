from django.apps import AppConfig
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.db.models.signals import post_migrate
from django.conf import settings
from .models import Articulo, Suscripcion, Comentario
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

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
        Permission.objects.get(codename='view_comentario', content_type=content_type_comentario),
        # Añade permisos para likes y dislikes si los tienes
    ]
    subscriber_group.permissions.set(permisos_suscriptor)

    # Permisos para Moderador
    permisos_moderador = [
        Permission.objects.get(codename='add_comentario', content_type=content_type_comentario),
        Permission.objects.get(codename='delete_comentario', content_type=content_type_comentario),
        Permission.objects.get(codename='change_comentario', content_type=content_type_comentario),
        Permission.objects.get(codename='view_comentario', content_type=content_type_comentario),
    ]
    moderator_group.permissions.set(permisos_moderador)

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