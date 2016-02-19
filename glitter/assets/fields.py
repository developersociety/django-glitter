# -*- coding: utf-8 -*-

from itertools import groupby

from django.db import models
from django.forms.models import ModelChoiceField, ModelChoiceIterator


class GroupedModelChoiceField(ModelChoiceField):
    def __init__(self, queryset, group_by_field='category', group_label=None, *args, **kwargs):
        """
        group_by_field is the name of a field on the model
        group_label is a function to return a label for each choice group
        """
        super(GroupedModelChoiceField, self).__init__(queryset, *args, **kwargs)
        self.group_by_field = group_by_field
        if group_label is None:
            self.group_label = lambda group: group
        else:
            self.group_label = group_label

        # Need correct ordering, and category titles
        self.queryset = self.queryset.select_related().order_by('category', 'title')

    def _get_choices(self):
        """
        Exactly as per ModelChoiceField except returns new iterator class
        """
        if hasattr(self, '_choices'):
            return self._choices
        return GroupedModelChoiceIterator(self)
    choices = property(_get_choices, ModelChoiceField._set_choices)


class GroupedModelChoiceIterator(ModelChoiceIterator):
    def __iter__(self):
        if self.field.empty_label is not None:
            yield ('', self.field.empty_label)

        if self.field.cache_choices:
            if self.field.choice_cache is None:
                self.field.choice_cache = [
                    (self.field.group_label(group), [self.choice(ch) for ch in choices])
                    for group, choices in groupby(
                        self.queryset.all(), key=lambda row: getattr(
                            row, self.field.group_by_field
                        )
                    )
                ]

            for choice in self.field.choice_cache:
                yield choice
        else:
            for group, choices in groupby(
                    self.queryset.all(),
                    key=lambda row: getattr(row, self.field.group_by_field)
            ):
                yield (self.field.group_label(group), [self.choice(ch) for ch in choices])


class AssetForeignKey(models.ForeignKey):
    def formfield(self, **kwargs):
        kwargs.setdefault('form_class', GroupedModelChoiceField)
        return super(AssetForeignKey, self).formfield(**kwargs)
