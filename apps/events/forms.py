#!/usr/bin/env python3

import logging

from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
import stripe

from . import models
from apps.tickets.models import Ticket
from utils.results import Success, Failure, Result

UUID_LAST_DIGITS = 12


logger = logging.getLogger(__name__)


class ProposalForm(forms.ModelForm):
    class Meta:
        model = models.Proposal
        fields = [
            "name",
            "surname",
            "email",
            "title",
            "description",
        ]

    def __init__(self, event, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update(
            {
                "id": "cfp-name",
                "size": "20",
                "placeholder": "Tu nombre",
                "class": "input is-rounded",
            }
        )
        self.fields["surname"].widget.attrs.update(
            {
                "id": "cfp-surname",
                "size": "40",
                "placeholder": "Tus apellidos",
                "class": "input is-rounded",
            }
        )
        self.fields["email"].widget.attrs.update(
            {
                "id": "cfp-email",
                "size": "40",
                "placeholder": "Tu email",
                "class": "input is-rounded",
            }
        )
        self.fields["title"].widget.attrs.update(
            {
                "id": "cfp-title",
                "size": "60",
                "placeholder": "El título de tu maravillosa charla",
                "class": "input is-rounded",
            }
        )
        self.fields["description"].widget.attrs.update(
            {
                "id": "cfp-title",
                "cols": "60",
                "rows": "20",
                "placeholder": ("El texto de tu maravillosa charla. "
                                "¿Aceptamos markdown? ¡Por supuesto!"),
                "class": "textarea",
            }
        )
        self.event = event

    def save(self):
        proposal = super().save(commit=False)
        proposal.event = self.event
        proposal.save()
        return proposal


class EmailForm(forms.Form):
    email = forms.EmailField(label="Tu email", max_length=192)


class WaitingListForm(forms.Form):

    email = forms.EmailField(label="Tu email", max_length=192)
    name = forms.CharField(label="Nombre", max_length=256)
    surname = forms.CharField(label="Apellidos", max_length=256)
    phone = forms.CharField(label="Teléfono", max_length=32)

    def __init__(self, event, *args, **kwargs):
        self.event = event
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        assert self.is_valid()
        wl = models.WaitingList(
            event=self.event,
            name=self.cleaned_data["name"],
            surname=self.cleaned_data["surname"],
            email=self.cleaned_data["email"],
            phone=self.cleaned_data["phone"],
            )
        if commit:
            wl.save()
        return wl


class RefundForm(forms.Form):

    email = forms.EmailField(label="Tu email", max_length=192)
    uuid = forms.CharField()

    def __init__(self, event, *args, **kwargs):
        logging.error("Llamada al metodo __init__ de RefundForm")
        super().__init__(*args, **kwargs)
        self.event = event

    def clean_uuid(self):
        email = self.cleaned_data["email"]
        uuid = self.cleaned_data["uuid"]
        if uuid == "tu puta madre":
            raise ValidationError("Cuida ese vocabulario")

        if len(uuid) < UUID_LAST_DIGITS:
            raise ValidationError(
                f"Necesito los últimos {UUID_LAST_DIGITS} letras o dígitos "
                "del código"
                )
        uuid = uuid[-UUID_LAST_DIGITS:]
        tickets = list(
            self.event.all_tickets()
            .filter(customer_email=email)
            .filter(keycode__iendswith=uuid)
        )
        if len(tickets) != 1:
            raise ValidationError(
                "El correo o las últimos {} letras o dígitos del"
                " codigo están mal.".format(UUID_LAST_DIGITS)
            )
        self.ticket = tickets[0]
        if models.Refund.exists(self.event, self.ticket):
            raise ValidationError(
                "Ya se ha solicitado una devolución del importe para ese ticket"
            )
        return uuid


class StripeForm(forms.Form):

    stripeEmail = forms.EmailField(label="Tu email", max_length=192)
    name = forms.CharField(label="Nombre propio", max_length=256)
    surname = forms.CharField(label="Apellidos", max_length=256)
    phone = forms.CharField(
        label='Teléfono',
        max_length=32,
        required=False,
        help_text=(
            'Opcional (Solo lo usaremos para resolver posibles problemas'
            ' con la compra de la entrada)'
            ),
        )
    url_privacy_policy = reverse_lazy('legal:privacy_policy')
    privacy_policy = forms.BooleanField(
        label='Política de Privacidad',
        help_text=mark_safe(
            'Acepto las  <a href="{url_privacy_policy}">Condiciones'
            ' generales de compra</a>.'
            ),
        )
    url_purchase_terms = reverse_lazy('legal:purchase_terms')
    purchase_terms = forms.BooleanField(
        label='Condiciones generales de compra',
        help_text=mark_safe(
            'Acepto las <a href="{url_purchase_terms}">'
            'Condiciones generales de compra'
            '</a>.'
            ),
        )
    stripeToken = forms.CharField(max_length=512)

    def __init__(self, article, *args, **kwargs):
        self.article = article
        super().__init__(*args, **kwargs)

    def charge_payment(self) -> Result:
        assert self.is_valid()
        email = self.cleaned_data["stripeEmail"]
        name = self.cleaned_data["name"]
        surname = self.cleaned_data["surname"]
        token = self.cleaned_data["stripeToken"]
        phone = self.cleaned_data.get("phone", None)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            customer = stripe.Customer.create(
                email=email,
                source=token,
                description="{}, {}".format(surname, name),
            )
            charge = stripe.Charge.create(
                customer=customer.id,
                amount=self.article.price_in_cents,
                currency="EUR",
                description="{}/{}, {}".format(
                    self.ticket.event.hashtag,
                    surname,
                    name,
                ),
            )
            if charge.paid:
                ticket = Ticket(
                    article=self.article,
                    customer_name=name,
                    customer_surname=surname,
                    customer_email=email,
                    customer_phone=phone,
                    payment_id=charge.id,
                )
                ticket.save()
                return Success({
                    'charge': charge,
                    'ticket': ticket,
                    })
            else:
                return Failure(
                    'Error al procesar el pago en Stripe',
                    extra={'charge': charge},
                    )
        except stripe.error.StripeError as err:
            logger.error(f"Error de stripe: {err}")
            return Failure(f"Error de stripe: {err}")
        except Exception as err:
            logger.error(f"Error interno: {err}")
            return Failure(f"Error interno: {err}")
