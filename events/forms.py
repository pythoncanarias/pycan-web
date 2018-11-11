from django import forms


class EmailForm(forms.Form):
    email = forms.EmailField(label='Tu email', max_length=192)


class WaitingListForm(forms.Form):
    email = forms.EmailField(label='Tu email', max_length=192)
    name = forms.CharField(label='Nombre', max_length=256)
    surname = forms.CharField(label='Apellidos', max_length=256)
    phone = forms.CharField(label='Teléfono', max_length=32)
