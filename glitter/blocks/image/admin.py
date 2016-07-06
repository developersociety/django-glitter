# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from glitter.blockadmin import blocks
from glitter.assets.widgets import ImageRelatedFieldWidgetWrapper, ImageSelect

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


blocks.site.register(ImageBlock, ImageBlockAdmin)
blocks.site.register_block(ImageBlock, 'Common')
