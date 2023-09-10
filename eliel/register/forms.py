from django import forms
from .models import Person
import re

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'inputBox', 'placeholder': 'Contraseña'}))
    
    class Meta:
        model = Person
        fields = ['nombre', 'correo_electronico', 'numero_telefono', 'password']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'inputBox', 'placeholder': 'Nombre de usuario'}),
            'correo_electronico': forms.EmailInput(attrs={'class': 'inputBox', 'placeholder': 'Correo electrónico'}),
            'numero_telefono': forms.TextInput(attrs={'class': 'inputBox', 'placeholder': 'Número de teléfono'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].label = "Nombre"
        self.fields['correo_electronico'].label = "Correo electrónico"
        self.fields['numero_telefono'].label = "Número de teléfono"
        self.fields['password'].label = "Contraseña"

    def clean_numero_telefono(self):
        numero_telefono = self.cleaned_data['numero_telefono']

        # Utilizamos una expresión regular para verificar el formato del número de teléfono (04xxxxxxxxx)
        if not re.match(r'^04\d{9}$', numero_telefono):
            raise forms.ValidationError("El número de teléfono debe tener el formato 04xxxxxxxxx.")

        return numero_telefono

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'inputBox', 'placeholder': 'Nombre de usuario'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'inputBox', 'placeholder': 'Contraseña'}))
