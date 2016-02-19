# -*- coding: utf-8 -*-

from django import forms


class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

    error_css_class = 'error'
    required_css_class = 'required'
