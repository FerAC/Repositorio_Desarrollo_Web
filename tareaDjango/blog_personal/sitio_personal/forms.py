from django import forms

class SubscriptionForm(forms.Form):
    email = forms.EmailField(label='Correo Electronico')
    nombre = forms.CharField(label='Nombre')
    frecuencia = forms.ChoiceField(choices=[('diario', 'Diario'), ('semanal', 'Semanal'), ('mensual', 'Mensual')],
                                   label='Frecuencia de Interaccion')
