# -*- coding: utf-8 -*-

from django.db import models
from django.forms.fields import EmailField

from mptt.fields import TreeForeignKey

from glitter.models import BaseBlock


class BaseFormBlock(BaseBlock):
    recipient = models.EmailField()
    success_page = TreeForeignKey('glitter_pages.Page', null=True, on_delete=models.SET_NULL)

    render_function = 'glitter.blocks.form.views.form_view'

    class Meta:
        abstract = True

    def get_replyto_address(self, form):
        email = None
        for name, field in form.base_fields.items():
            if type(field) == EmailField:
                email = form.cleaned_data[name]
                break
        return email


class BaseFormNoEmailBlock(BaseBlock):
    success_page = TreeForeignKey('glitter_pages.Page', null=True, on_delete=models.SET_NULL)

    render_function = 'glitter.blocks.form.views.form_view'

    class Meta:
        abstract = True


class ContactFormBlock(BaseFormBlock):
    form_class = 'glitter.blocks.form.forms.ContactForm'

    class Meta:
        verbose_name = 'contact form'
