# Generated by Django 4.2.13 on 2024-05-12 23:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sitio_personal', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='articulo',
            name='preview',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='articulo',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='thumbnails/'),
        ),
        migrations.AddField(
            model_name='articulo',
            name='tiempo_lectura',
            field=models.IntegerField(default=5),
        ),
    ]
