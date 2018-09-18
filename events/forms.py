from django import forms

class EmailForm(forms.Form):
    email = forms.EmailField(label='Tu email', max_length=192)
