# -*- coding: utf-8 -*-
from importlib import import_module

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.mail import EmailMessage
from django.core.urlresolvers import get_mod_func
from django.forms import ModelForm
from django.forms.fields import FileField
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils import six

from glitter.exceptions import GlitterRedirectException

from .models import BaseFormBlock, BaseFormNoEmailBlock
from .signals import form_valid


def form_view(block, request, rerender, content_block, block_classes, form_class=None):
    css_classes = ' '.join(block_classes)

    # Get the form class from the model
    if form_class is None:
        form_class = getattr(type(block), 'form_class', None)

    # Get the callable version of the form
    if isinstance(form_class, six.string_types):
        mod_name, class_name = get_mod_func(form_class)
        form_class = getattr(import_module(mod_name), class_name)

    if form_class is None:
        raise ImproperlyConfigured(
            "Form block %s requires a form_class attribute, or the render_function for %s needs"
            " to give a form_class" % (block, block))

    if isinstance(block, BaseFormBlock) and (not block.recipient or not block.success_page):
        # Need a recipient and a page to redirect to - so can't display form
        form = None
    elif isinstance(block, BaseFormNoEmailBlock) and not block.success_page:
        # Just need a success page - so can't display form
        form = None
    elif rerender:
        # Don't process a form on a rerender
        form = form_class()
    else:
        # All should be okay to process the form!
        form = form_class(request.POST or None, request.FILES or None)

        if form.is_valid():
            version = content_block.obj_version
            obj = version.content_object

            # Fire a signal if more functionality is needed
            form_valid.send(
                sender=form_class, request=request, form=form, obj=obj, version=version)

            # Save any model forms
            if isinstance(form, ModelForm):
                model_obj = form.save(commit=False)

                # Allow object tweaking if needed
                if hasattr(model_obj, 'pre_save'):
                    model_obj.pre_save(request=request)

                model_obj.save()

            # Don't send emails for this form block
            if isinstance(block, BaseFormNoEmailBlock):
                raise GlitterRedirectException(block.success_page.url)

            # Additional information for emailing
            page_url = '%s://%s%s' % (request.scheme, request.get_host(), obj.get_absolute_url())

            email_subject = settings.EMAIL_SUBJECT_PREFIX + block._meta.verbose_name
            email_body = render_to_string('glitter/form_email.txt', {
                'form': form,
                'obj': obj,
                'page_url': page_url,
            })
            email = EmailMessage(
                subject=email_subject,
                body=email_body,
                to=[block.recipient])

            # Add any attachments
            if form.is_multipart():
                for field in form:
                    if isinstance(field.field, FileField):
                        file_upload = form.cleaned_data[field.name]

                        if file_upload:
                            file_upload.open('rb')
                            file_content = file_upload.read()
                            email.attach(filename=file_upload.name, content=file_content)

            email.send(fail_silently=False)
            raise GlitterRedirectException(block.success_page.url)

    return render_to_string((
        'glitter/blocks/%s.html' % (block._meta.model_name,),
        'glitter/blocks/formblock.html',
    ), {
        'content_block': content_block,
        'css_classes': css_classes,
        'object': block,
        'form': form,
    }, context_instance=RequestContext(request))
