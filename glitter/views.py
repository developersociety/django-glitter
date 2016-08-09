# -*- coding: utf-8 -*-

from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render_to_response
from django.utils.encoding import force_text
from django.views.decorators.csrf import csrf_protect

from glitter.models import Version
from glitter.page import Glitter


@csrf_protect
def render_page(request, page, page_version, edit=False):
    glitter = Glitter(page_version, request=request)
    columns = glitter.render(edit_mode=edit)

    template_name = page_version.template_name
    context = {
        'glitter': glitter,
        'edit_mode': edit,
        'columns': columns,
        page._meta.model_name: page,
        'object': page}

    return render_to_response(template_name, context)


@csrf_protect
def render_object_unpublished(request, obj):
    info = obj._meta.app_label, obj._meta.model_name
    verbose_name = force_text(obj._meta.verbose_name)

    # Users without the edit permission for this object get a 404 instead of object not published
    if not request.user.has_perm('%s.edit_%s' % info):
        raise Http404('No published %(verbose_name)s available' % {
            'verbose_name': verbose_name,
        })

    # Find the latest version a user has access to
    version = Version.objects.filter(
        content_type=ContentType.objects.get_for_model(obj), object_id=obj.id).exclude(
        ~Q(owner=request.user), version_number__isnull=True).first()

    if version is not None:
        next_url = reverse('admin:%s_%s_version' % info, kwargs={'version_id': version.id})
    else:
        # No version available, go edit a new template
        next_url = reverse('admin:%s_%s_template' % info, kwargs={'object_id': obj.id})

    template_name = 'admin/glitter/object_unpublished.html'
    context = {
        'object': obj,
        'version': version,
        'next_url': next_url,
        'verbose_name': verbose_name}

    response = render_to_response(template_name, context)
    return response
