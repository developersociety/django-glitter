======
Blocks
======


On a page, a block is a chunk of content which sits in a column.

With Glitter, a block is a combination of a Django model and a template file,
registered with the block admin so it can be selected in frontend templates.


Quick example
=============

This example block defines a ``HeadlineText`` model, with just one attribute
named ``text`` in ``models.py``.

.. code:: python

    from django.db import models

    from glitter.models import BaseBlock


    class HeadlineText(BaseBlock):
        text = models.TextField()


To make this usable in the frontend, we need to register this block in
``blocks.py``.

.. code:: python

    from glitter.blockadmin import blocks

    from .models import HeadlineText


    @blocks.register(HeadlineText, category='Common')
    class HeadlineTextAdmin(blocks.BlockAdmin):
        pass


Which works with the template ``glitter/blocks/headlinetext.html``.

.. code:: html

    <div class="{{ css_classes }}">
        {{ object.text }}
    </div>


Discovery of blocks
===================

Glitter will automatically look for a ``blocks`` module in each application and
import it. This allows you to keep the block registration in your project in a
well known and consistent location - ``blocks.py``.


Models
======

A block is just a Django model which extends from ``BaseBlock``. Any number of
additional fields can be added as attributes.

In this example, we create a new model ``Link``, with two attributes ``text``
and ``url`` - both of which are Django model fields::

    from django.db import models

    from glitter.models import BaseBlock


    class Link(BaseBlock):
        text = models.CharField(max_length=100)
        url = models.URLField('URL')


**Note**: Avoid using ``models.FileField`` and ``models.ImageField``, these are
currently not recommended.


Registration
============

To register a block so it can be selected in the frontend when editing a page,
the block needs to be registered with the Glitter block admin. By default this
belongs in ``blocks.py``.

In this example, we're registering the ``Link`` model from earlier::

    from glitter.blockadmin import blocks

    from .models import Link


    @blocks.register(Link, category='Common')
    class LinkAdmin(blocks.BlockAdmin):
        pass


Alternatively it's possible to use the ``blocks.site.register`` function
instead of the ``blocks.register`` decorator::

    blocks.site.register(Link, category='Common')


Multiple blocks can be registered at once with ``blocks.site.register``::

    blocks.site.register((HeadlineText, Link), category='Common')


We can also use a custom ``BlockAdmin``, however the decorator is preferred as
a cleaner way of registering blocks in this case::

    blocks.site.register(HeadlineText, HeadlineTextAdmin, category='Common')


Templates
=========

By default the template name used for rendering the block is based on the name
of the block class, converted to lowercase.

The template for this would be ``glitter/blocks/link.html``::

    class Link(BaseBlock):
        text = models.CharField(max_length=100)
        url = models.URLField('URL')


A default fallback template is used if this doesn't exist, which uses the
``__str__`` method to show some content::

    <div class="{{ css_classes }}">
        {{ object }}
    </div>


To show some meaningful content for the ``Link`` block example from earlier,
we need to customise it::

    <div class="{{ css_classes }}">
        <a href="{{ object.url }}">{{ object.text }}</a>
    </div>
