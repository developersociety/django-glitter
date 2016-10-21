from django.contrib.contenttypes.models import ContentType
from django.test import TestCase, modify_settings, override_settings

from glitter.models import Version
from glitter.page import Glitter
from glitter.pages.models import Page


class TestGlitterDefaultBlocks(TestCase):
    def setUp(self):
        self.page = Page.objects.create(url='/test/', title='Test page')
        self.page_version = Version.objects.create(
            content_type=ContentType.objects.get_for_model(Page),
            object_id=self.page.id,
            template_name='glitter/sample.html',
        )
        self.glitter = Glitter(self.page_version)

    @override_settings(
        GLITTER_DEFAULT_BLOCKS=None,
    )
    @modify_settings(INSTALLED_APPS={
        'append': 'glitter.blocks.image',
    })
    def test_default_blocks(self):
        # Standard blocks: Text, Image, HTML
        self.assertEqual(
            self.glitter.default_blocks, [
                ('glitter_redactor.Redactor', 'Text'),
                ('glitter_image.ImageBlock', 'Image'),
                ('glitter_html.HTML', 'HTML'),
            ],
        )

    @override_settings(
        GLITTER_DEFAULT_BLOCKS=[('glitter_html.HTML', 'HTML')],
    )
    def test_custom_blocks(self):
        # Custom will return whatever is given to it
        self.assertEqual(self.glitter.default_blocks, [('glitter_html.HTML', 'HTML')])
