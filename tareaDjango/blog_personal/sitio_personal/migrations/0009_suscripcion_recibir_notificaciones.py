# Generated by Django 4.2.13 on 2024-05-21 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sitio_personal', '0008_mensajecontacto'),
    ]

    operations = [
        migrations.AddField(
            model_name='suscripcion',
            name='recibir_notificaciones',
            field=models.BooleanField(default=False),
        ),
    ]