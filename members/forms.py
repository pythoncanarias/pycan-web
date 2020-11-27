from django import forms

from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Id. Usuario',
        strip=True,
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        strip=True,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def clean_password(self):
        """Validate username/password.
        It everything is OK, the `user` attribute of the
        form is set to the authenticated user.
        """
        username = self.cleaned_data.get('username', '')
        password = self.cleaned_data.get('password', '')
        if username and password:
            self.user = authenticate(username=username, password=password)
            if self.user is None:
                raise ValidationError(
                    "La contraseña pare este identificador del usuario"
                    " es incorrecta."
                )
        return password
