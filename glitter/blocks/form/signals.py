import django.dispatch


form_valid = django.dispatch.Signal(providing_args=['request', 'form', 'obj', 'version'])
