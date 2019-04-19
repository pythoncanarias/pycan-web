import logging

from django import forms

from .models import Refund

UUID_LAST_DIGITS = 12


class EmailForm(forms.Form):
    email = forms.EmailField(label='Tu email', max_length=192)


class WaitingListForm(forms.Form):
    email = forms.EmailField(label='Tu email', max_length=192)
    name = forms.CharField(label='Nombre', max_length=256)
    surname = forms.CharField(label='Apellidos', max_length=256)
    phone = forms.CharField(label='Teléfono', max_length=32)


class RefundForm(forms.Form):
    email = forms.EmailField(label='Tu email', max_length=192)
    uuid = forms.CharField()

    def __init__(self, event, *args, **kwargs):
        logging.error('Llamada al metodo __init__ de RefundForm')
        super().__init__(*args, **kwargs)
        self.event = event

    def clean_uuid(self):
        email = self.cleaned_data["email"]
        uuid = self.cleaned_data["uuid"]
        if uuid == 'tu puta madre':
            raise forms.ValidationError('Cuida ese vocabulario')

        if len(uuid) < UUID_LAST_DIGITS:
            raise forms.ValidationError(
                'Necesito los últimos () letras o dígitos '
                'del código'.format(UUID_LAST_DIGITS)
                )
        uuid = uuid[-UUID_LAST_DIGITS:]
        tickets = list(
            self.event.all_tickets()
            .filter(customer_email=email)
            .filter(keycode__iendswith=uuid)
            )
        if len(tickets) != 1:
            raise forms.ValidationError(
                'El correo o las últimos {} letras o dígitos del'
                ' codigo están mal.'.format(UUID_LAST_DIGITS)
                )
        self.ticket = tickets[0]
        if Refund.exists(self.event, self.ticket):
            raise forms.ValidationError(
                'Ya se ha solicitado una devolución del'
                ' importe para ese ticket'
                )
        return uuid
