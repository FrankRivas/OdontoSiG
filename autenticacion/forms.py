from django import forms
from django.contrib.auth.models import User
from material import *

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', ]

    layout = Layout(Fieldset('Agregar Usuario: '), Row('username', 'email'), Row('first_name', 'last_name'))

    def __init__(self, *args, **kwargs):
        super(UsuarioForm, self).__init__(*args, **kwargs)
        self.fields['email'].unique = True
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        users = User.objects.all()
        for user in users:
            if user.email.lower() == email:
                raise forms.ValidationError("¡Ya existe un usuario con ese email!")
        return email
