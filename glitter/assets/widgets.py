# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.admin.sites import AdminSite
from django.contrib.admin.templatetags.admin_static import static
from django.contrib.admin.views.main import IS_POPUP_VAR, TO_FIELD_VAR
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django.core.urlresolvers import reverse
from django.forms.widgets import Media, Select
from django.template.loader import render_to_string

from glitter.templatetags.glitter_admin_js import jquery_min
from glitter.assets.models import ImageCategory


LIMIT_IMAGES_TO = 20


class ImageRelatedFieldWidgetWrapper(RelatedFieldWidgetWrapper):
    def get_related_url(self, info, action, *args):
        url_params = '&'.join("%s=%s" % param for param in [
            (TO_FIELD_VAR, self.rel.get_related_field().name),
            (IS_POPUP_VAR, 1),
        ])

        return '{}?{}'.format(
            reverse(
                "admin:%s_%s_%s" % (info + (action,)), current_app=AdminSite(), args=args
            ), url_params
        )

    def render(self, name, value, *args, **kwargs):
        rel_to = self.rel.to
        info = (rel_to._meta.app_label, rel_to._meta.object_name.lower())
        self.widget.choices = self.choices
        context = self.widget.render(name, value, *args, **kwargs)
        context['name'] = name

        if self.can_add_related:
            related_url = self.get_related_url(info, 'add')
            context['can_add_related_url'] = related_url

        if self.can_change_related:
            related_url = self.get_related_url(info, 'change', '__fk__')
            context['can_change_related_url'] = related_url

        rendered = render_to_string(
            'admin/glitter/widgets/image_related_field.html', context
        )
        return rendered

    @property
    def media(self):
        js_media = Media(
            js=[
                jquery_min(),
                static('admin/js/related-widget-wrapper.js'),
                static('glitter/libs/dropzonejs/dropzone.min.js'),
                static('glitter/js/widgets/image_dropzone.js'),
            ],
        )
        css_media = Media(
            css={
                'all': (static('glitter/css/widgets/images.min.css'),)
            }
        )
        return self.widget.media + js_media + css_media


class ImageSelect(Select):
    class Media:
        css = {
            'all': ('glitter/css/widgets/images.min.css',)
        }
        js = ('glitter/js/widgets/images.js',)

    def render(self, name, value, attrs=None, choices=()):

        if value is None:
            value = ''
        options = self.render_options(choices, [value])

        context = {
            'options': options,
            'images': self.choices.queryset.order_by(
                '-created_at', 'modified_at', 'title'
            )[:LIMIT_IMAGES_TO],
            'categories': ImageCategory.objects.all()
        }
        return context
