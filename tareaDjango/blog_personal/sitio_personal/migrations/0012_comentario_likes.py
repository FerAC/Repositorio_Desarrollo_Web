# Generated by Django 4.2.13 on 2024-06-14 05:35

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sitio_personal', '0011_comentario_usuario'),
    ]

    operations = [
        migrations.AddField(
            model_name='comentario',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='likes_coment', to=settings.AUTH_USER_MODEL),
        ),
    ]
