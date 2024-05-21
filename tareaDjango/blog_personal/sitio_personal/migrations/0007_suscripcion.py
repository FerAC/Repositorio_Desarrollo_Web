# Generated by Django 4.2.13 on 2024-05-20 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sitio_personal', '0006_comentario_es_respuesta'),
    ]

    operations = [
        migrations.CreateModel(
            name='Suscripcion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('nombre', models.CharField(max_length=100)),
                ('frecuencia', models.CharField(choices=[('diario', 'Diario'), ('semanal', 'Semanal'), ('mensual', 'Mensual')], max_length=10)),
                ('fecha_suscripcion', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]