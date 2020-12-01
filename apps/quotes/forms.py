#!/usr/bin/env python

from django import forms

from .models import Quote


class QuoteForm(forms.ModelForm):

    class Meta:
        model = Quote
        exclude = []

    text = forms.CharField(widget=forms.Textarea(
        attrs={'rows': 5, 'cols': 68}
    ))
