# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from collections import namedtuple

from django.apps import apps
from django.db.models.base import ModelBase
from django.utils import six

from .layouts import PageLayoutBase


Template = namedtuple('Template', ['layout', 'model'])


def register(class_or_iterable, model_class):
    if isinstance(class_or_iterable, PageLayoutBase):
        class_or_iterable = [class_or_iterable]

    for layout in class_or_iterable:
        template_name = layout._meta.template

        # Find the model class given a string if needed
        if not isinstance(model_class, ModelBase):
            model_class = apps.get_model(model_class)

        templates[template_name] = Template(layout=layout, model=model_class)


def get_templates(model):
    """ Return a list of templates usable by a model. """
    for template_name, template in six.iteritems(templates):
        if issubclass(template.model, model):
            yield (template_name, template.layout._meta.verbose_name)


def get_layout(template_name):
    """ Return a registered layout from a template name. """
    return templates[template_name].layout


def attach(*layouts, **kwargs):
    """
    Registers the given layout(s) classes
    admin site:

    @pages.register(Page)
    class Default(PageLayout):
        pass
    """

    def _model_admin_wrapper(layout_class):
        register(layout_class, layouts[0])
        return layout_class
    return _model_admin_wrapper

templates = {}
