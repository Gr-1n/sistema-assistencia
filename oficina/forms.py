from django import forms
from django.contrib.auth.forms import AuthenticationForm

class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Define o valor inicial como 'adm'
        self.fields['username'].initial = 'adm'
        self.fields['password'].initial = 'adm'
        
        # Aproveitando para garantir que as classes do Bootstrap estejam aqui
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget = forms.PasswordInput(render_value=True)
        self.fields['password'].widget.attrs.update({'class': 'form-control'})