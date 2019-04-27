from django import forms


class NewMemberForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    password_shadow = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_shadow = cleaned_data.get('password_shadow')

        if password != password_shadow:
            raise forms.ValidationError('No coinciden las contraseñas')
