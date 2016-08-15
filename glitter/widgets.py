# -*- coding: utf-8 -*-

import django
from django.contrib.admin.sites import AdminSite
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django.core.urlresolvers import reverse
from django.forms.widgets import Select


class AddBlockSelect(Select):
    def render_options(self, choices, selected_choices):
        header = '<option value="" disabled="" selected="">Add a block:</option>'
        options = super(AddBlockSelect, self).render_options(choices, selected_choices)
        return header + options


class ChooseColumnSelect(Select):
    def render_options(self, choices, selected_choices):
        header = '<option value="" disabled="">Choose column:</option>'
        options = super(ChooseColumnSelect, self).render_options(choices, selected_choices)
        return header + options


class MoveBlockSelect(Select):
    def render_options(self, choices, selected_choices):
        header = '<option value="" disabled="" selected="">Move block:</option>'
        options = super(MoveBlockSelect, self).render_options(choices, selected_choices)
        return header + options


class CustomRelatedFieldWidgetWrapper(RelatedFieldWidgetWrapper):
    def get_related_url(self, info, action, *args):
        current_app = AdminSite()
        if django.VERSION >= (1, 9):
            current_app = None
        viewname = "admin:%s_%s_%s" % (info + (action,))
        return reverse(viewname, current_app=current_app, args=args)
