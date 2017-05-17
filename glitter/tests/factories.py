from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType

import factory

from glitter.models import Version
from glitter.pages.models import Page


class PageFactory(factory.DjangoModelFactory):
    url = factory.Sequence(lambda n: '/page-{}/'.format(n))
    title = factory.Sequence(lambda n: 'Page {}'.format(n))

    class Meta:
        model = Page


class VersionFactory(factory.DjangoModelFactory):
    object_id = factory.SelfAttribute('content_object.id')
    content_type = factory.LazyAttribute(
        lambda o: ContentType.objects.get_for_model(o.content_object),
    )

    class Meta:
        exclude = ('content_object',)
        abstract = True


class PageVersionFactory(VersionFactory):
    content_object = factory.SubFactory(PageFactory)

    class Meta:
        model = Version

    @factory.post_generation
    def set_version(self, create, extracted, **kwargs):
        if extracted:
            page = self.content_object
            page.current_version = self

            if create:
                page.save()
