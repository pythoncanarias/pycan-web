from django import forms

from django.contrib.auth.models import User

from apps.members.models import Member
from apps.members.models import Membership

class NewMemberForm(forms.Form):
    first_name = forms.CharField(label="Nombre", max_length=150)
    last_name = forms.CharField(label="Apellidos", max_length=150)
    email = forms.EmailField(label="Correo electrónico")
    address = forms.CharField(label="Dirección", max_length=100)
    rest_address = forms.CharField(label="Dirección", max_length=100)
    postal_code = forms.CharField(label='C.P.', max_length=10)
    city = forms.CharField(label="Ciudad", max_length=64)
    phone = forms.CharField(label='Teléfono',  max_length=20)
    payment_date = forms.DateField(label='Fecha de pago')
    payment_reference = forms.CharField(label='Referencia del pago', max_length=128)

    def set_widget(self, name, klass, **kwargs):
        kwargs['class'] = klass
        self.fields[name].widget.attrs.update(**kwargs)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_widget('first_name', 'input is-rounded',
            size=20,
            placeholder="Nombre",
            )
        self.set_widget('last_name', 'input is-rounded',
            size=40,
            placeholder="Apellidos",
            )
        self.set_widget('email', 'input is-rounded',
            size=40,
            placeholder="Email",
            )
        self.set_widget('address', 'input is-rounded',
            size=60,
            placeholder="Dirección (primera línea)",
            )
        self.set_widget('rest_address', 'input is-rounded',
            size=60,
            placeholder="Dirección (segunda línea)",
            )
        self.set_widget('postal_code', 'input is-rounded',
            size=10,
            placeholder="Código postal",
            )
        self.set_widget('city', 'input is-rounded',
            size=64,
            placeholder="Ciudad",
            )
        self.set_widget('phone', 'input is-rounded',
            size=64,
            placeholder="Teléfono",
            )
        self.set_widget('payment_date', 'input is-rounded',
            size=64,
            placeholder="Fecha del pago",
            )
        self.set_widget('payment_reference', 'input is-rounded',
            size=64,
            placeholder="Referencia del pago",
            )

