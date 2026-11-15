from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


def validate_username_is_unique(username):
    _User = get_user_model()
    if _User.objects.filter(username=username).count() > 0:
        raise ValidationError(
                f"El username elegido: {username} ya existe, "
                " tiene que elegir otro valor."
                )


def validate_email_is_unique(email):
    _User = get_user_model()
    if _User.objects.filter(email=email).count() > 0:
        raise ValidationError(
                f"El correo electrónico elegido: {email} ya existe, "
                " tiene que elegir otro valor."
                )


class NewMemberForm(forms.Form):
    first_name = forms.CharField(
        label="Nombre",
        max_length=150,
        required=True,
        )
    last_name = forms.CharField(
        label="Apellidos",
        max_length=150,
        required=True,
        )
    email = forms.EmailField(
        label="Correo electrónico",
        required=True,
        validators=[
            validate_email_is_unique,
            ],
        )
    username = forms.SlugField(
        label="Login / Username",
        required=True,
        validators=[
            validate_username_is_unique,
            ],
        )
    address = forms.CharField(
        label="Dirección",
        max_length=100,
        required=True,
        )
    rest_address = forms.CharField(
        label="Dirección (Segunda línea opcional)",
        max_length=100,
        required=False,
        )
    postal_code = forms.CharField(
        label='Código postal',
        max_length=10,
        required=True,
        )
    city = forms.CharField(
        label="Ciudad / Población",
        max_length=64,
        required=True,
        )
    phone = forms.CharField(
        label='Teléfono',
        max_length=20,
        required=False,
        )
    payment_date = forms.DateField(
        label='Fecha de pago',
        required=True,
        )
    payment_reference = forms.CharField(
        label='Referencia del pago',
        max_length=128,
        required=False,
        )

    def set_widget(self, name, klass='', **kwargs):
        _field = self.fields[name]
        if klass:
            if 'class' in kwargs:
                actual_class = kwargs['class']
                if klass not in actual_class:
                    kwargs['class'] = f'{actual_class} {klass}'
            else:
                kwargs['class'] = klass
        if _field.widget.__class__.__name__ == 'TextInput':
            if hasattr(self.fields[name], 'label'):
                kwargs['placeholder'] = self.fields[name].label
        _field.widget.attrs.update(**kwargs)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_widget('first_name', 'input is-rounded', size=20)
        self.set_widget('last_name', 'input is-rounded', size=40)
        self.set_widget('email', 'input is-rounded', size=40)
        self.set_widget('username', 'input is-rounded', size=40)
        self.set_widget('address', 'input is-rounded', size=60)
        self.set_widget('rest_address', 'input is-rounded', size=60)
        self.set_widget('postal_code', 'input is-rounded', size=10)
        self.set_widget('city', 'input is-rounded', size=64)
        self.set_widget('phone', 'input is-rounded', size=64)
        self.set_widget('payment_date', 'input is-rounded', size=64)
        self.set_widget('payment_reference', 'input is-rounded', size=64)
