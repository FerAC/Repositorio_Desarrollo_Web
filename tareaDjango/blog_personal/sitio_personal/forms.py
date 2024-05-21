from django import forms
from .models import Comentario, MensajeContacto

class SubscriptionForm(forms.Form):
    email = forms.EmailField(label='Correo Electrónico')
    nombre = forms.CharField(label='Nombre')
    frecuencia = forms.ChoiceField(
        choices=[('diario', 'Diario'), ('semanal', 'Semanal'), ('mensual', 'Mensual')],
        label='Frecuencia de Interacción'
    )
    recibir_notificaciones = forms.BooleanField(label='Recibir notificaciones de nuevos artículos', required=False)

class ContactForm(forms.ModelForm):
    class Meta:
        model = MensajeContacto
        fields = ['nombre', 'email', 'cuerpo']
        labels = {
            'nombre': 'Nombre',
            'email': 'Correo Electrónico',
            'cuerpo': 'Mensaje'
        }


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['nombre', 'cuerpo']
