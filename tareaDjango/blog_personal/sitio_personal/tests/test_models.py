import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_personal.settings')
import django
django.setup()

from django.test import TestCase
from sitio_personal.models import Suscripcion
from sitio_personal.models import Etiqueta
from sitio_personal.models import Articulo
from sitio_personal.models import Comentario
from sitio_personal.models import MensajeContacto



class EtiquetaTestCase(TestCase):
    def setUp(self):
        # Crea un objeto Etiqueta para usar en las pruebas
        self.etiqueta = Etiqueta.objects.create(
            nombre='Python'
        )

    def test_str_representation(self):
        # Verifica que el método __str__ funcione correctamente
        self.assertEqual(str(self.etiqueta), 'Python')

class ArticuloTestCase(TestCase):
    def setUp(self):
        # Crea un objeto Etiqueta para asociarlo al artículo
        self.etiqueta = Etiqueta.objects.create(nombre='Python')

        # Crea un objeto Articulo para usar en las pruebas
        self.articulo = Articulo.objects.create(
            titulo='Título del artículo',
            contenido='Contenido del artículo',
            thumbnail=None,
            preview='Vista previa del contenido',
            tiempo_lectura=10
        )
        self.articulo.etiquetas.add(self.etiqueta)

    def test_str_representation(self):
        # Verifica que el método __str__ funcione correctamente
        self.assertEqual(str(self.articulo), 'Título del artículo')

    def test_thumbnail_name(self):
        # Verifica que el método thumbnail_name devuelva el nombre de la miniatura
        self.assertIsNone(self.articulo.thumbnail_name())

    def test_total_likes(self):
        # Verifica que el método total_likes devuelva la cantidad correcta de likes
        self.assertEqual(self.articulo.total_likes(), 0)

class ComentarioTestCase(TestCase):
    def setUp(self):
        # Crea un objeto Articulo para asociarlo al comentario
        self.articulo = Articulo.objects.create(
            titulo='Título del artículo',
            contenido='Contenido del artículo'
        )

        # Crea un objeto Comentario para usar en las pruebas
        self.comentario = Comentario.objects.create(
            articulo=self.articulo,
            nombre='Autor del comentario',
            cuerpo='Cuerpo del comentario',
            parent=None,
            es_respuesta=False
        )

    def test_str_representation(self):
        # Verifica que el método __str__ funcione correctamente
        expected_str = f'Comentario de Autor del comentario en {self.articulo}'
        self.assertEqual(str(self.comentario), expected_str)

    def test_is_reply(self):
        # Verifica que el método is_reply detecte correctamente si el comentario es una respuesta
        self.assertFalse(self.comentario.is_reply())

class SuscripcionTestCase(TestCase):
    def test_str_representation(self):
        # Crea un objeto Suscripcion para usar en las pruebas
        suscripcion = Suscripcion.objects.create(
            email='test@example.com',
            nombre='Test User',
            frecuencia='diario',
            recibir_notificaciones=True
        )
        # Verifica que el método __str__ funcione correctamente
        self.assertEqual(str(suscripcion), 'Test User (test@example.com)')

class MensajeContactoTestCase(TestCase):
    def test_str_representation(self):
        # Crea un objeto MensajeContacto para usar en las pruebas
        mensaje = MensajeContacto.objects.create(
            nombre='John Doe',
            email='john.doe@example.com',
            cuerpo='Este es un mensaje de prueba.'
        )
        # Verifica que el método __str__ funcione correctamente
        self.assertEqual(str(mensaje), 'Mensaje de John Doe (john.doe@example.com)')

