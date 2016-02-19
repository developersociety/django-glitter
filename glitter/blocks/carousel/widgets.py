# -*- coding: utf-8 -*-

from django.contrib.admin.sites import AdminSite
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django.core.urlresolvers import reverse


class CustomRelatedFieldWidgetWrapper(RelatedFieldWidgetWrapper):

    def get_related_url(self, info, action, *args):
        return reverse(
            "admin:%s_%s_%s" % (info + (action,)), current_app=AdminSite(), args=args
        )
