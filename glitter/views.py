# -*- coding: utf-8 -*-

from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.encoding import force_text
from django.views.decorators.csrf import csrf_protect

from glitter.models import Version
from glitter.page import Glitter


@csrf_protect
def render_page(request, page, page_version, edit=False):
    glitter = Glitter(page_version, request=request)
    columns = glitter.render(edit_mode=edit)

    return render_to_response(page_version.template_name, {
        'glitter': glitter,
        'edit_mode': edit,
        'columns': columns,
        page._meta.model_name: page,
        'object': page,
    }, context_instance=RequestContext(request))


@csrf_protect
def render_object_unpublished(request, obj):
    info = obj._meta.app_label, obj._meta.model_name
    verbose_name = force_text(obj._meta.verbose_name)

    # Users without the edit permission for this object get a 404 instead of object not published
    edit_permission = '%s.edit_%s' % info
    has_edit_permission = (
        request.user.has_perm(edit_permission) or
        request.user.has_perm(edit_permission, obj=obj)
    )

    if not has_edit_permission:
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

    response = render_to_response('admin/glitter/object_unpublished.html', {
        'object': obj,
        'version': version,
        'next_url': next_url,
        'verbose_name': verbose_name,
    }, context_instance=RequestContext(request))

    return response
