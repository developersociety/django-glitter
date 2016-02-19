# -*- coding: utf-8 -*-

from collections import OrderedDict
import inspect

from django.forms.forms import pretty_name
from django.template.defaultfilters import title
from django.utils import six
from django.utils.text import camel_case_to_spaces

from .columns import Column


class Options(object):
    def __init__(self, meta, cls):
        self.template = ''
        self.verbose_name = ''
        self.columns = {}

        self._update_template(cls, meta)
        self._update_verbose_name(cls, meta)

    def _update_template(self, cls, meta):
        if hasattr(meta, 'template'):
            self.template = meta.template
        else:
            self.template = 'glitter/{}.html'.format(cls.__name__.lower())

    def _update_verbose_name(self, cls, meta):
        if hasattr(meta, 'verbose_name'):
            self.verbose_name = meta.verbose_name
        else:
            self.verbose_name = title(camel_case_to_spaces(cls.__name__))


class PageLayoutBase(type):
    """
    Base Layout meta class used to store template structure details.
    """

    def __new__(cls, name, bases, attrs):
        super_new = super(PageLayoutBase, cls).__new__

        # (excluding PageLayout class itself).
        # Also ensure initialization is only performed for subclasses of PageLayout
        parents = [b for b in bases if isinstance(b, PageLayoutBase)]
        if not parents:
            new_class = super_new(cls, name, bases, attrs)
            return new_class

        attr_meta = attrs.pop('Meta', None)
        module = attrs.pop('__module__')
        new_class = super_new(cls, name, bases, {'__module__': module})
        if not attr_meta:
            meta = getattr(new_class, 'Meta', None)
        else:
            meta = attr_meta

        # Create meta API.
        meta = Options(meta, new_class)

        # If columns are inherited merge them with new colums.
        if hasattr(new_class, '_meta'):
            if new_class._meta.columns:
                attrs.update(new_class._meta.columns)

        if issubclass(new_class, PageLayout):
            # Columns
            columns = {}
            for column, cls in six.iteritems(attrs):
                if isinstance(cls, Column):
                    columns.setdefault(column, cls)

            columns = sorted(columns.items(), key=lambda x: getattr(x[1], 'creation_counter'))

            meta.columns = OrderedDict(columns)

        new_class.add_to_class('_meta', meta)

        return new_class

    def add_to_class(cls, name, value):
        # We should call the contribute_to_class method only if it's bound
        if not inspect.isclass(value) and hasattr(value, 'contribute_to_class'):
            value.contribute_to_class(cls, name)
        else:
            setattr(cls, name, value)

    def get_column_name(self, column_name):
        """ Get a column for given column name from META api. """
        name = pretty_name(column_name)
        if column_name in self._meta.columns:
            column_cls = self._meta.columns[column_name]
            if column_cls.verbose_name:
                name = column_cls.verbose_name
        return name


class PageLayout(six.with_metaclass(PageLayoutBase)):
    pass
