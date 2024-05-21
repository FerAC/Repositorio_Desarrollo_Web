from django.urls import reverse
from django.core import mail
from django.conf import settings
from sitio_personal.models import Articulo, Etiqueta
from sitio_personal.forms import ContactForm
from sitio_personal.models import MensajeContacto
from sitio_personal.views import enviar_correo_bienvenida
import pytest

def test_index_view(client):
    # Simula una solicitud GET a la vista index
    response = client.get(reverse('index'))

    # Verifica que la solicitud fue exitosa (código de respuesta 200)
    assert response.status_code == 200

    # Verifica que la plantilla correcta se está utilizando
    assert 'sitio_personal/index.html' in [template.name for template in response.templates]


def test_blog_view(client):
    # Simula una solicitud GET a la vista blog
    response = client.get(reverse('blog'))

    # Verifica que la solicitud fue exitosa (código de respuesta 200)
    assert response.status_code == 200

    # Verifica que la plantilla correcta se está utilizando
    assert 'sitio_personal/blog.html' in [template.name for template in response.templates]


def test_resume_view(client):
    # Simula una solicitud GET a la vista resume
    response = client.get(reverse('resume'))

    # Verifica que la solicitud fue exitosa (código de respuesta 200)
    assert response.status_code == 200

    # Verifica que la plantilla correcta se está utilizando
    assert 'sitio_personal/resume.html' in [template.name for template in response.templates]


def test_about_view(client):
    # Simula una solicitud GET a la vista about
    response = client.get(reverse('about'))

    # Verifica que la solicitud fue exitosa (código de respuesta 200)
    assert response.status_code == 200

    # Verifica que la plantilla correcta se está utilizando
    assert 'sitio_personal/about.html' in [template.name for template in response.templates]


@pytest.fixture
def create_objects(django_db_setup):
    # Crea objetos Articulo y Etiqueta para usar en las pruebas
    etiqueta1 = Etiqueta.objects.create(nombre='Python')
    etiqueta2 = Etiqueta.objects.create(nombre='Django')
    articulo1 = Articulo.objects.create(titulo='Título del artículo 1', contenido='Contenido del artículo 1')
    articulo2 = Articulo.objects.create(titulo='Título del artículo 2', contenido='Contenido del artículo 2')
    articulo1.etiquetas.add(etiqueta1)
    articulo2.etiquetas.add(etiqueta2)
    return etiqueta1, etiqueta2, articulo1, articulo2


@pytest.mark.django_db
def test_contact_view_get(client):
    """
    Prueba que la vista contact renderiza correctamente con una solicitud GET.
    """
    response = client.get(reverse('contacto'))
    assert response.status_code == 200
    assert 'sitio_personal/contacto.html' in [template.name for template in response.templates]
    assert isinstance(response.context['form'], ContactForm)


@pytest.mark.django_db
def test_contact_view_post_valid(client):
    """
    Prueba que la vista contact maneja correctamente una solicitud POST con datos válidos.
    """
    form_data = {
        'nombre': 'Test User',
        'email': 'test@example.com',
        'cuerpo': 'Este es un mensaje de prueba.',
    }
    response = client.post(reverse('contacto'), data=form_data)

    # Verifica que la respuesta redirige a la plantilla de éxito
    assert response.status_code == 200
    assert 'sitio_personal/contacto_exitoso.html' in [template.name for template in response.templates]

    # Verifica que el correo electrónico fue enviado
    assert len(mail.outbox) == 1
    email = mail.outbox[0]
    assert email.subject == 'Nuevo mensaje de contacto'
    assert 'Nombre: Test User' in email.body
    assert 'Email: test@example.com' in email.body
    assert 'Mensaje:\nEste es un mensaje de prueba.' in email.body

    # Verifica que el mensaje de contacto fue guardado en la base de datos
    assert MensajeContacto.objects.count() == 1
    mensaje = MensajeContacto.objects.first()
    assert mensaje.nombre == 'Test User'
    assert mensaje.email == 'test@example.com'
    assert mensaje.cuerpo == 'Este es un mensaje de prueba.'


@pytest.mark.django_db
def test_contact_view_post_invalid(client):
    """
    Prueba que la vista contact maneja correctamente una solicitud POST con datos inválidos.
    """
    form_data = {
        'nombre': '',
        'email': 'test@example.com',
        'cuerpo': '',
    }
    response = client.post(reverse('contacto'), data=form_data)

    # Verifica que la respuesta vuelve a renderizar el formulario con errores
    assert response.status_code == 200
    assert 'sitio_personal/contacto.html' in [template.name for template in response.templates]
    assert isinstance(response.context['form'], ContactForm)
    assert response.context['form'].errors
    assert 'nombre' in response.context['form'].errors
    assert 'cuerpo' in response.context['form'].errors


@pytest.mark.django_db
def test_detalle_articulo_view(client):
    """
    Prueba que la vista detalle_articulo renderiza correctamente con un articulo_id válido.
    """
    articulo = Articulo.objects.create(
        titulo='Título del artículo',
        contenido='Contenido del artículo'
    )

    response = client.get(reverse('detalle_articulo', args=[articulo.id]))
    assert response.status_code == 200
    assert 'sitio_personal/detalle_articulo.html' in [template.name for template in response.templates]
    assert response.context['articulo'] == articulo


@pytest.mark.django_db
def test_detalle_articulo_view_not_found(client):
    """
    Prueba que la vista detalle_articulo devuelve un 404 con un articulo_id no válido.
    """
    response = client.get(reverse('detalle_articulo', args=[999]))
    assert response.status_code == 404


@pytest.mark.django_db
def test_enviar_correo_bienvenida(mailoutbox):
    """
    Prueba que la función enviar_correo_bienvenida envía un correo correctamente.
    """
    email = 'test@example.com'
    nombre = 'Test User'
    enviar_correo_bienvenida(email, nombre)

    # Verifica que un correo ha sido enviado
    assert len(mailoutbox) == 1

    # Verifica que el correo tiene el asunto correcto
    assert mailoutbox[0].subject == 'Bienvenido a mi Blog'

    # Verifica que el correo tiene el mensaje correcto
    assert mailoutbox[0].body == f'Hola {nombre},\n\nGracias por suscribirte a mi blog. ¡Saludos!'

    # Verifica que el correo ha sido enviado desde la dirección correcta
    assert mailoutbox[0].from_email == settings.DEFAULT_FROM_EMAIL

    # Verifica que el correo ha sido enviado a la dirección correcta
    assert mailoutbox[0].to == [email]