# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.conf.urls import url
from django.forms.forms import pretty_name
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.template import Context
from django.template.loader import get_template

from glitter.assets.forms import ImageForm
from glitter.assets.models import Image
from glitter.assets.widgets import LIMIT_IMAGES_TO, ImageRelatedFieldWidgetWrapper, ImageSelect
from glitter.blockadmin import blocks

from .forms import ImageBlockForm
from .models import ImageBlock


class ImageBlockAdmin(blocks.BlockAdmin):
    form = ImageBlockForm

    def formfield_for_dbfield(self, db_field, **kwargs):
        """
        Hook for specifying the form Field instance for a given database Field
        instance.

        If kwargs are given, they're passed to the form Field's constructor.
        """
        formfield = super(ImageBlockAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'image':
            formfield.widget = ImageRelatedFieldWidgetWrapper(
                ImageSelect(), db_field.rel, self.admin_site, can_add_related=True,
                can_change_related=True,
            )
        return formfield

    def get_urls(self):
        urls = super(ImageBlockAdmin, self).get_urls()
        app_label, model_name = self.model._meta.app_label, self.model._meta.model_name
        image_block_urls = [
            url(r'^get-lazy-images/$', self.get_lazy_images, name='get-lazy-images'),
            url(
                r'^drop-image/$',
                self.drop_image,
                name='{app_label}_{model_name}_drop_image'.format(
                    app_label=app_label, model_name=model_name
                )
            ),
        ]
        return image_block_urls + urls

    def get_lazy_images(self, request):
        last_image_id = request.GET.get('last_image_id', None)
        if last_image_id and last_image_id.isdigit():
            images = Image.objects.filter(
                id__lt=last_image_id
            ).order_by(
                '-created_at', 'modified_at', 'title'
            )[:LIMIT_IMAGES_TO]
            template = get_template('glitter/blocks/includes/lazy_images.html')
            context = Context({'images': images})
            html = template.render(context)
            return JsonResponse({'html': html, 'last_image_id': last_image_id})
        else:
            response = JsonResponse({'error': 'No last image id passed'})
            response.status_code = 400

        return response

    def drop_image(self, request):

        permission_name = '{}.edit_{}'.format(self.opts.app_label, self.opts.model_name)
        if not request.user.has_perm(permission_name):
            return HttpResponseForbidden('403 Forbidden', content_type='text/html')

        form = ImageForm(request.POST, request.FILES or None)
        if form.is_valid():
            filename, ext = os.path.splitext(form.files['file'].name)
            filename = pretty_name(filename)

            image = form.save(commit=False)
            image.title = filename
            image.save()
            return JsonResponse({'image_id': image.id, 'filename': filename})
        else:
            message = ''
            for field_name, error_list in form.errors.items():
                message = '{field} - {message}'.format(
                    field=field_name.capitalize(), message=''.join(error_list)
                )
                return HttpResponse(message, status=403)


blocks.site.register(ImageBlock, ImageBlockAdmin)
blocks.site.register_block(ImageBlock, 'Common')
