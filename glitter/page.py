# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from collections import OrderedDict, defaultdict
from importlib import import_module

from django.apps import apps
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import get_mod_func, reverse
from django.db.models import Q
from django.forms.widgets import Select
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string
from django.utils import six
from django.utils.encoding import force_text
from django.utils.functional import cached_property
from django.utils.http import urlencode
from django.utils.text import capfirst

from .models import Version
from .templates import get_layout, get_templates
from .widgets import AddBlockSelect, ChooseColumnSelect, MoveBlockSelect

# If no other settings are provided, show text/image/HTML blocks
GLITTER_FALLBACK_BLOCKS = (
    'glitter_redactor.Redactor',
    'glitter_image.ImageBlock',
    'glitter_html.HTML',
)


class GlitterBlock(object):
    def __init__(self, content_block, column, block_number):
        self.content_block = content_block
        self.block = content_block.content_object
        self.column = column
        self.glitter_page = column.glitter_page
        self.block_number = block_number

    def render(self, rerender):
        # Add some classes to the block to help style it
        block_classes = self.css_classes()

        # Render the block
        mod_name, func_name = get_mod_func(self.block.render_function)
        block_view = getattr(import_module(mod_name), func_name)

        self.html = block_view(
            self.block, self.glitter_page.request, rerender, self.content_block, block_classes
        )

    def css_classes(self):
        # Add some classes to the block to help style it

        block_classes = ['glitter_page_blocktype_{}'.format(self.block._meta.model_name)]

        if self.block_number == 1:
            block_classes.append('glitter_page_block_first')

        if self.block_number % 2 == 0:
            block_classes.append('glitter_page_block glitter_page_block_even')
        else:
            block_classes.append('glitter_page_block glitter_page_block_odd')

        if self.block_number == len(self.column.blocks):
            block_classes.append('glitter_page_block_last')

        return block_classes

    def block_type(self):
        """ This gets display on the block header. """
        return capfirst(force_text(
            self.content_block.content_type.model_class()._meta.verbose_name
        ))

    def edit_url(self):
        opts = self.block._meta.app_label, self.block._meta.model_name
        return reverse('block_admin:%s_%s_change' % opts, args=(self.block.pk,))

    def choose_column_widget(self):
        column_options = self.glitter_page.get_column_choices()

        widget = ChooseColumnSelect(attrs={
            'class': 'glitter-move-column-select',
        }, choices=column_options)

        return widget.render(name='', value=self.column.name)

    def move_block_widget(self):
        # Imported here due to circular imports
        from glitter.forms import MoveBlockForm

        move_options = []

        if self.block_number != 1:
            move_options.extend((
                (MoveBlockForm.MOVE_TOP, 'To top'),
                (MoveBlockForm.MOVE_UP, 'Up'),
            ))

        if self.block_number != len(self.column.blocks):
            move_options.extend((
                (MoveBlockForm.MOVE_DOWN, 'Down'),
                (MoveBlockForm.MOVE_BOTTOM, 'To bottom'),
            ))

        widget = MoveBlockSelect(attrs={
            'class': 'glitter-move-block-select',
        }, choices=move_options)

        return widget.render(name='', value=None)


class GlitterColumn(object):
    def __init__(self, name, verbose_name, glitter_page, content_blocks):
        self.name = name
        self.verbose_name = verbose_name
        self.glitter_page = glitter_page
        self.blocks = []

        # Build up a list of page blocks
        for block_num, content_block in enumerate(content_blocks, start=1):
            block = GlitterBlock(content_block, self, block_num)
            self.blocks.append(block)

    def render(self, edit_mode=False, rerender=False):
        # Render all the blocks
        for block in self.blocks:
            block.render(rerender)

        # Column structure
        column_template = 'glitter/include/column.html'
        column_context = {
            'blocks': self.blocks,
            'column_slug': slugify(self.name),
        }

        if edit_mode:
            # Edit mode has a more complex template
            column_template = 'glitter/include/column_edit.html'

            column_context.update({
                'glitter': self.glitter_page,
                'verbose_name': self.verbose_name,
                'default_blocks_top': self.get_default_blocks(top=True),
                'default_blocks_bottom': self.get_default_blocks(),
                'add_block_widget_top': self.add_block_widget(top=True),
                'add_block_widget_bottom': self.add_block_widget(),
            })

        return render_to_string(column_template, column_context)

    def get_default_blocks(self, top=False):
        """
        Return a list of column default block tuples (URL, verbose name).

        Used for quick add block buttons.
        """
        default_blocks = []

        for block_model, block_name in self.glitter_page.default_blocks:
            block = apps.get_model(block_model)
            base_url = reverse('block_admin:{}_{}_add'.format(
                block._meta.app_label, block._meta.model_name,
            ), kwargs={
                'version_id': self.glitter_page.version.id,
            })
            block_qs = {
                'column': self.name,
                'top': top,
            }
            block_url = '{}?{}'.format(base_url, urlencode(block_qs))
            block_text = capfirst(force_text(block._meta.verbose_name))

            default_blocks.append((block_url, block_text))

        return default_blocks

    def add_block_widget(self, top=False):
        """
        Return a select widget for blocks which can be added to this column.
        """
        widget = AddBlockSelect(attrs={
            'class': 'glitter-add-block-select',
        }, choices=self.add_block_options(top=top))

        return widget.render(name='', value=None)

    def add_block_options(self, top):
        """
        Return a list of URLs and titles for blocks which can be added to this column.

        All available blocks are grouped by block category.
        """
        from .blockadmin import blocks

        block_choices = []

        # Group all block by category
        for category in sorted(blocks.site.block_list):
            category_blocks = blocks.site.block_list[category]
            category_choices = []

            for block in category_blocks:
                base_url = reverse('block_admin:{}_{}_add'.format(
                    block._meta.app_label, block._meta.model_name,
                ), kwargs={
                    'version_id': self.glitter_page.version.id,
                })
                block_qs = {
                    'column': self.name,
                    'top': top,
                }
                block_url = '{}?{}'.format(base_url, urlencode(block_qs))
                block_text = capfirst(force_text(block._meta.verbose_name))

                category_choices.append((block_url, block_text))

            category_choices = sorted(category_choices, key=lambda x: x[1])
            block_choices.append((category, category_choices))

        return block_choices


class Glitter(object):
    """
    A page object which contains all of the data necessary to render a glitter template.
    """

    saved_pages = None
    unsaved_pages = None

    def __init__(self, page_version, request=None):
        self.version = page_version
        self.obj = page_version.content_object
        self.content_type = ContentType.objects.get_for_model(self.obj)
        self.opts = self.obj._meta
        self.request = request

        if request is None:
            self.user = None
        else:
            self.user = request.user

        self.layout = get_layout(template_name=page_version.template_name)

        # Only show controls to logged in users
        if self.user is not None:
            self.show_controls = self.user.has_perm(
                '%s.edit_%s' % (self.opts.app_label, self.opts.model_name))
        else:
            self.show_controls = False

        # Fetch all content blocks in one go
        self.column_blocks = defaultdict(list)
        content_blocks = self.version.contentblock_set.select_related(
            'content_type'
        ).prefetch_related('content_object').all()

        for content_block in content_blocks:
            # As ContentBlock links to blocks using GenericForeignKey, it's possible to delete a
            # block and for the ContentBlock to still exist. We need to filter them out to prevent
            # any errors.
            if content_block.content_object is not None:
                self.column_blocks[content_block.column].append(content_block)

    def render(self, edit_mode=False, rerender=False):
        columns = OrderedDict()

        for column_name in self.layout._meta.columns:
            verbose_name = self.layout.get_column_name(column_name)

            column = GlitterColumn(
                name=column_name,
                verbose_name=verbose_name,
                glitter_page=self,
                content_blocks=self.column_blocks[column_name]
            )
            columns[column_name] = column.render(edit_mode=edit_mode, rerender=rerender)

        return columns

    def owner_versions(self):
        # Fiddly queryset which hides unsaved versions of other users
        return Version.objects.select_related('owner').filter(
            content_type=self.content_type, object_id=self.obj.id).exclude(
            ~Q(owner=self.user), version_number__isnull=True
        )

    def all_versions(self):
        return self.owner_versions().order_by('-modified')

    @cached_property
    def previous_version(self):
        try:
            return self.owner_versions().filter(
                modified__lt=self.version.modified).order_by('-modified')[0]
        except IndexError:
            return None

    @cached_property
    def next_version(self):
        try:
            return self.owner_versions().filter(
                modified__gt=self.version.modified
            ).order_by('modified')[0]
        except IndexError:
            return None

    def change_template_widget(self):
        change_template_options = sorted(get_templates(self.obj.__class__), key=lambda x: x[1])

        widget = Select(attrs={
            'id': 'id_template_name',
        }, choices=change_template_options)

        return widget.render(name='template_name', value=self.layout._meta.template)

    def get_column_choices(self):
        choices = []
        for column, cls in six.iteritems(self.layout._meta.columns):
            name = self.layout.get_column_name(column)
            choices.append((column, name))
        return choices

    @cached_property
    def default_blocks(self):
        """
        Return a list of default block tuples (appname.ModelName, verbose name).

        Next to the dropdown list of block types, a small number of common blocks which are
        frequently used can be added immediately to a column with one click. This method defines
        the list of default blocks.
        """
        # Use the block list provided by settings if it's defined
        block_list = getattr(settings, 'GLITTER_DEFAULT_BLOCKS', None)

        if block_list is not None:
            return block_list

        # Try and auto fill in default blocks if the apps are installed
        block_list = []

        for block in GLITTER_FALLBACK_BLOCKS:
            app_name, model_name = block.split('.')

            try:
                model_class = apps.get_model(app_name, model_name)
                verbose_name = capfirst(model_class._meta.verbose_name)
                block_list.append((block, verbose_name))
            except LookupError:
                # Block isn't installed - don't add it as a quick add default
                pass

        return block_list

    def has_add_permission(self):
        """
        Returns a boolean if the current user has permission to add another object of the same
        type which is being viewed/edited.
        """
        has_permission = False

        if self.user is not None:
            # We don't check for the object level permission - as the add permission doesn't make
            # sense on a per object level here.
            has_permission = self.user.has_perm(
                '{}.add_{}'.format(self.opts.app_label, self.opts.model_name)
            )

        return has_permission

    def has_change_permission(self):
        """
        Returns a boolean if the current user has permission to change the current object being
        viewed/edited.
        """
        has_permission = False

        if self.user is not None:
            # We check for the object level permission here, even though by default the Django
            # admin doesn't. If the Django ModelAdmin is extended to allow object level
            # permissions - then this will work as expected.
            permission_name = '{}.change_{}'.format(self.opts.app_label, self.opts.model_name)
            has_permission = (
                self.user.has_perm(permission_name) or
                self.user.has_perm(permission_name, obj=self.obj)
            )

        return has_permission

    def has_edit_permission(self):
        """
        Returns a boolean if the current user has permission to edit the current object being
        viewed/edited.
        """
        has_permission = False

        if self.user is not None:
            permission_name = '{}.edit_{}'.format(self.opts.app_label, self.opts.model_name)
            has_permission = (
                self.user.has_perm(permission_name) or
                self.user.has_perm(permission_name, obj=self.obj)
            )

        return has_permission

    def has_publish_permission(self):
        """
        Returns a boolean if the current user has permission to publish the current object being
        viewed/edited.
        """
        has_permission = False

        if self.user is not None:
            permission_name = '{}.publish_{}'.format(self.opts.app_label, self.opts.model_name)
            has_permission = (
                self.user.has_perm(permission_name) or
                self.user.has_perm(permission_name, obj=self.obj)
            )

        return has_permission
