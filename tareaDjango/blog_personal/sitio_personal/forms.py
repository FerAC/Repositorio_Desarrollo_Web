from django import forms
from .models import Comentario, MensajeContacto

class SubscriptionForm(forms.Form):
    """
    Formulario de suscripción al blog.

    Permite a los usuarios suscribirse al blog con su correo electrónico,
    nombre y seleccionar la frecuencia de interacción deseada.
    """
    email = forms.EmailField(label='Correo Electrónico')
    nombre = forms.CharField(label='Nombre')
    frecuencia = forms.ChoiceField(
        choices=[('diario', 'Diario'), ('semanal', 'Semanal'), ('mensual', 'Mensual')],
        label='Frecuencia de Interacción'
    )
    recibir_notificaciones = forms.BooleanField(
        label='Recibir notificaciones de nuevos artículos',
        required=False
    )

class ContactForm(forms.ModelForm):
    """
    Formulario de contacto.

    Permite a los usuarios enviar mensajes de contacto con su nombre,
    correo electrónico y cuerpo del mensaje.
    """
    class Meta:
        model = MensajeContacto
        fields = ['nombre', 'email', 'cuerpo']
        labels = {
            'nombre': 'Nombre',
            'email': 'Correo Electrónico',
            'cuerpo': 'Mensaje'
        }

class ComentarioForm(forms.ModelForm):
    """
    Formulario de comentario.

    Permite a los usuarios agregar comentarios con su nombre y el cuerpo del comentario.
    """
    class Meta:
        model = Comentario
        fields = ['nombre', 'cuerpo']
