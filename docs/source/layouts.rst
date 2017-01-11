=======
Layouts
=======


Glitter templates render a list of columns in a Django template, with each Glitter model having a
defined number of layouts.


Quick example
=============

This example layout defines a ``Default`` layout with 3 columns, ``content``, ``sidebar`` and
``footer``, registered to the Glitter Pages model.

.. code:: python

    from glitter import columns, templates
    from glitter.layouts import PageLayout


    @templates.attach('glitter_pages.Page')
    class Default(PageLayout):
        content = columns.Column(width=640)
        sidebar = columns.Column(width=320)
        footer = columns.Column(width=960)

Which works with the following template ``glitter/default.html``.

.. code:: html

    <main>
        <aside>
            {{ columns.sidebar }}
        </aside>
        <article>
            {{ columns.content }}
        </article>
    </main>
    <footer>
        {{ columns.footer }}
    </footer>


Discovery of layouts
====================

Glitter will automatically look for a ``layouts`` module in each application and imports it. This
allows you to keep your layouts in your project in a well known and consistent location -
``layouts.py``.


Columns
=======

The most important part of a layout - the columns of content which will be rendered into the
template. Columns are specified by class attributes.

Example:

.. code:: python

    from glitter import columns
    from glitter.layouts import PageLayout


    class Default(PageLayout):
        content = columns.Column(width=640)


Attributes
----------

`width`

    The width of the column in pixels. Any blocks which render images can use this data to
    thumbnail any large images to an appropriate width.


Verbose column names
--------------------

Columns take an optional first argument - a verbose name. If a verbose name isn't given, Glitter
will automatically create it from the attribute name, converting any underscores to spaces.

In this example, the verbose name is ``'Main content'``::

    content = columns.Column('Main content', width=640)

In this example, the verbose name is ``'Left column'``::

    left_column = columns.Column(width=640)


Registering a layout
====================

To use a layout with a Glitter model, it needs to be registered. The ``templates.attach`` decorator
registers a layout to be used with that model.

The attach decorator can either be passed a ``'app_label.model_name'`` string, or the model class.

This example registers 2 layouts, a ``Default`` layout which can be used with Glitter Pages, and a
``NewsPost`` layout which is registered with a news application's ``Post`` model.

.. code:: python

    from glitter import columns, templates
    from glitter.layouts import PageLayout
    from news.models import Post


    @templates.attach('glitter_pages.Page')
    class Default(PageLayout):
        content = columns.Column(width=640)


    @templates.attach(Post)
    class NewsPost(PageLayout):
        content = columns.Column(width=640)


Template name
=============

By default the template name used for rendering the layout is based on the name of the layout
class, converted to lowercase.

The template for this would be ``glitter/newspost.html``::

    class NewsPost(PageLayout):
        content = columns.Column(width=640)

If a custom template name is needed to keep the templates for one app in one directory, we can
define this as a ``template`` attribute in the ``Meta`` class for the layout::

    class Document(PageLayout):
        content = columns.Column(width=960)

        class Meta:
            template = 'documents/document_detail.html'
