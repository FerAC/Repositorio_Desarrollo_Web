from django import forms
from .models import Comentario

class SubscriptionForm(forms.Form):
    email = forms.EmailField(label='Correo Electronico')
    nombre = forms.CharField(label='Nombre')
    frecuencia = forms.ChoiceField(choices=[('diario', 'Diario'), ('semanal', 'Semanal'), ('mensual', 'Mensual')],
                                   label='Frecuencia de Interaccion')

class ContactForm(forms.Form):
    email = forms.EmailField(label='Correo electronico', max_length=100)
    name = forms.CharField(label='Nombre', max_length=100)
    message = forms.CharField(label='Mensaje', widget=forms.Textarea)


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['nombre', 'cuerpo']
