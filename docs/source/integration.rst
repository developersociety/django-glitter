==========================================
Integrating other Django Apps into Glitter
==========================================

Glitter App Pages
=================

Pages for standard Django Apps can be added to Glitter's page hierarchy easily by using the Glitter
App Pages feature, which allows:

* standard Django apps to appear in the navigation alongside Glitter Pages
* admin users to be able to set the URL & menu position for standard Glitter apps
* integration with page selection widgets and other bits & bobs which rely on the Glitter Page
  structure.

Instructions
------------

1) Add/create/magic-up a standard Django app to your project as you normally would

2) Ensure the Django app has a root (`r'^$',`) route in its `urls.py`. For example, the Glitter
   News app has the following root route in `glitter_news/urls.py`::

       urlpatterns = [
           url(
               r'^$',
               views.PostListView.as_view(),
               name='list'
           ),

           ...
        ]

3) Setup your project's main `urls.py` to support Glitter App Pages by removing any existing URLs
   you might have for the Django apps you're integrating into Glitter. If you don't remove these,
   then they tend to conflict with the Glitter App Pages and you'll get unpredictable results.

4) Include `glitter.urls` into your project's main `urls.py` by adding this line to your
   `urlpatterns`::

       urlpatterns = [
           ...

           url(r'^', include('glitter.urls')),

           ...
       ]

5) Create a `glitter_apps.py` file in the app. This will tell Glitter that the app supports
   Glitter App Pages, where to find the app's URLs and sets a human friendly name.

   Glitter News's `glitter_news/glitter_apps.py` file looks like this::

       from glitter.integration import GlitterApp


       apps = {
           'glitter_news': GlitterApp(
               name='Glitter News', url_conf='glitter_news.urls', namespace='glitter-news',
           ),
       }

   Here, `glitter_news` is a unique name for the configuration. It's important this is unique as
   it's used for lookups later on... so name it something sensible.

   The `name='Glitter News'` is setting a human friendly name which will be used in the next steps.

   `url_conf='glitter_news.urls', namespace='glitter-news'` are the same value you'd normally enter
   (and probably just removed) in your project's `urls.py`.

6) Restart your web server. This is required to ensure Glitter has the latest version of the
   `glitter_apps.py` files.

7) In the Django Admin, add a new Glitter Page. You should notice the name of your Glitter App
   appears in the Advanced Options. Select that, and now when you go to that page's URL, you'll
   see your standard Django app.
