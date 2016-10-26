========================
Adding Glitter to an app
========================

Most Django models can use Glitter, which should be as easy as adding a mixin
to the model you want to use, and a mixin to the ``DetailView`` used to render
any objects for the model.


Glitter models
==============

Adding glitter to a model involves changing the class the model extends from,
as well as the ``Meta`` class if you need one.

Here's an example of an existing model::

    from django.db import models


    class Post(models.Model):
        title = models.CharField(max_length=100, db_index=True)
        date = models.DateTimeField(default=timezone.now, db_index=True)

        class Meta:
            ordering = ('-date',)

We change the parent class to ``GlitterMixin``, and extend the Meta class from
``GlitterMixin.Meta``::

    from django.db import models

    from glitter.mixins import GlitterMixin


    class Post(GlitterMixin):
        title = models.CharField(max_length=100, db_index=True)
        date = models.DateTimeField(default=timezone.now, db_index=True)

        class Meta(GlitterMixin.Meta):
            ordering = ('-date',)

After adding the mixin, we need to make migrations for the model and migrate
the database.

.. code:: console

    $ python manage.py makemigrations
    $ python manage.py migrate


The Glitter Mixin
-----------------

The mixin currently adds 2 fields to the model, ``published`` and
``current_version`` - both of which aren't editable in the Django admin, but
are needed to store data.

Additional permissions are also added with the mixin, *edit* allows a user to
edit new Glitter pages for an object - but not edit the object itself,
*published* allows a user to change the current published version of a Glitter
object.


Glitter Manager
---------------

The default manager for Glitter models adds two queryset methods for
convenience.

``Model.objects.published()``

    Any objects which are published.

``Model.objects.unpublished()``

    Any objects which aren't published.


Detail view
===========

After adding the model mixin, we need to add a mixin to the detail view and
adjust it slightly.

Using our Post example from earlier, here's an existing detail view::

    from django.views.generic import DetailView

    from .models import Post


    class PostDetailView(DetailView):
        model = Post

We need to add the ``GlitterDetailMixin``::

    from django.views.generic import DetailView

    from glitter.mixins import GlitterDetailMixin

    from .models import Post


    class PostDetailView(GlitterDetailMixin, DetailView):
        model = Post


List views
==========

Glitter objects which don't have any page versions saved or published shouldn't
be visible to frontend viewers, so we'll need to change any list views to
filter these out.

Using our Post example from earlier, here's an existing list view::

    from django.views.generic import ListView

    from .models import Post


    class PostListView(ListView):
        model = Post

We need to add to change the queryset::

    from django.views.generic import ListView

    from .models import Post


    class PostListView(ListView):
        queryset = Post.objects.published()
