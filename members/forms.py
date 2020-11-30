from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.contrib.auth import update_session_auth_hash


MIN_PASSWORD_LENGTH = 8

# Validation error messages

WRONG_PASSWORD = (
    "La contraseña para este identificador de usuario"
    " es incorrecta."
    )

PASSWORD_USES_USERNAME = (
    "La contraseña no debería contener el id. de usuario"
    )

PASSWORD_TOO_SHORT = (
    f"La contraseña es demasiado corta"
    f" (Mínimo {MIN_PASSWORD_LENGTH} letras)"
    )

OLD_PASSWORD_IS_WRONG = "La contraseña anterior es incorrecta"

NEW_PASSWORD_DOES_NOT_MATCH = (
    "La nueva contraseña y la contraseña de confirmación"
    " no coinciden"
    )


class LoginForm(forms.Form):

    error_css_class = 'error'
    required_css_class = 'required'

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
        self.fields['username'].widget.attrs.update({
            'class': "input",
            'size': '40',
        })
        self.fields['password'].widget.attrs.update({
            'class': "input",
            'size': '40',
        })
        self.user = None

    def clean_username(self):
        """Validate username is not too short.
        """
        username = self.cleaned_data.get('username', '')
        if len(username) < 2:
            raise ValidationError(
                "El identificador de usuario es demasiado corto"
            )
        return username

    def clean_password(self):
        """Validate username/password.
        It everything is OK, the `user` attribute of the
        form is set to the authenticated user.
        """
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        self.user = authenticate(username=username, password=password)
        if self.user is None:
            raise ValidationError(WRONG_PASSWORD)
        return password


class PasswordChangeForm(forms.Form):

    old_password = forms.CharField(
        label="Password anterior",
        widget=forms.PasswordInput(render_value=True),
        strip=True,
    )
    new_password = forms.CharField(
        label="Nuevo password",
        widget=forms.PasswordInput(render_value=True),
        strip=True,
    )
    new_password_again = forms.CharField(
        label="Nuevo password (Confirmación)",
        widget=forms.PasswordInput(render_value=True),
        strip=True,
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({
            'class': "input",
            'size': '40',
        })
        self.fields['new_password'].widget.attrs.update({
            'class': "input",
            'size': '40',
        })
        self.fields['new_password_again'].widget.attrs.update({
            'class': "input",
            'size': '40',
        })

    def clean_old_password(self):
        old_password = self.cleaned_data['old_password']
        _usr = authenticate(
            username=self.user.username,
            password=old_password,
            )
        if _usr is None:
            raise ValidationError(OLD_PASSWORD_IS_WRONG)
        return old_password

    def clean_new_password(self):
        new_password = self.cleaned_data['new_password']
        if len(new_password) < MIN_PASSWORD_LENGTH:
            raise ValidationError(PASSWORD_TOO_SHORT)
        if self.user.username in new_password:
            raise ValidationError(PASSWORD_USES_USERNAME)
        return new_password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data['new_password']
        new_password_again = cleaned_data['new_password_again']
        if new_password != new_password_again:
            raise ValidationError(NEW_PASSWORD_DOES_NOT_MATCH)
        return cleaned_data

    def save(self, request):
        new_password = self.cleaned_data['new_password']
        self.user.set_password(new_password)
        self.user.save()
        update_session_auth_hash(request, self.user)
        messages.success(request, "Contraseña cambiada correctamente")

