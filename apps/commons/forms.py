from django import forms
from django.forms import widgets


class BaseForm(forms.Form):
    """Formulario generico adaptado para Bulma.css
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            widget = visible.field.widget
            match widget.__class__:
                case widgets.Select:
                    widget.attrs['class'] = 'select is-fullwidth'
                case widgets.Textarea:
                    widget.attrs['class'] = 'textarea'
                case widgets.FileInput:
                    widget.attrs['class'] = 'file-input'
                case widgets.RadioSelect:
                    widget.attrs['class'] = 'radio'
                case widgets.CheckboxInput:
                    widget.attrs['class'] = 'checkbox'
                case _:
                    widget.attrs['class'] = 'input'


class ModelBaseForm(BaseForm, forms.ModelForm):
    pass



class EstaSeguro(BaseForm):
    """Formulario para autorizar operaciones críticas.

    Solo será válido si se ha marcado el checkbox.
    """

    esta_seguro = forms.BooleanField(
        required=True,
        initial=False,
        label='¿Está seguro?',
        help_text='Por favor, confirme la operación',
        )


