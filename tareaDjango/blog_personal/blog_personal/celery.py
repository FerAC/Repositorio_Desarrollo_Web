from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Establece el entorno de Django para Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_personal.settings')

app = Celery('blog_personal')

# Usa la configuración de Django para Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descubre y carga tareas de todas las aplicaciones Django registradas
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')