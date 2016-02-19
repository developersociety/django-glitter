import django.dispatch


page_version_saved = django.dispatch.Signal(providing_args=['obj', 'version', 'user'])
page_version_published = django.dispatch.Signal(providing_args=[
    'obj', 'version', 'previous_version', 'user'
])
page_version_unpublished = django.dispatch.Signal(providing_args=['obj', 'version', 'user'])
