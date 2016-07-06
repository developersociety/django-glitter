============
Installation
============


Getting the code
----------------



The recommended way to install the Debug Toolbar is via pip_::

    $ pip install django-glitter

If you aren't familiar with pip, you may also obtain a copy of the
``glitter`` directory and add it to your Python path.

.. _pip: http://www.pip-installer.org/


Installation
------------


You will need to add the ``glitter`` application to the `INSTALLED_APPS`
setting of your Django project ``settings.py`` file.::

    INSTALLED_APPS = (
        #...
        'glitter',
        'glitter.pages',
        #...
    )


.. note::

    We need to mention here about our required packages ``django-mptt``,
    ``django-mptt-admin``, ``sorl-thumbnail`` and hint users to add in
    `INSTALLED_APPS`.

.. note::

    Explain diffences between ``glitter`` and ``glitter.pages``


URLconf
-------

Add the ``glitter`` URLs to your project's URLconf as follows::

    from glitter import block_admin

    urlpatterns = [
        #...
        url(r'^blockadmin/', include(block_admin.site.urls)),
        #...
    ]


Middleware
----------

Each time any Django application raises a 404 error, this
``glitter.pages.middleware.PageFallbackMiddleware`` middleware checks the
glitter pages database for the requested URL as a last resort

The middleware ``glitter.middleware.ExceptionMiddleware`` is handles
exceptions if the object doesn't have the current version or hasn't been
published it prompts the user to create a new page it also deals with blocks
which raise exception ``GlitterRedirectException``::


    MIDDLEWARE_CLASSES = [
        #...
        'glitter.pages.middleware.PageFallbackMiddleware',
        'glitter.middleware.ExceptionMiddleware',
        #...
    ]
