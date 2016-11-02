from django.contrib.contenttypes.models import ContentType
from django.test import TestCase, modify_settings, override_settings

from glitter.blocks.html.models import HTML
from glitter.models import ContentBlock, Version
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


class TestGlitterQueries(TestCase):
    def setUp(self):
        self.page = Page.objects.create(url='/test/', title='Test page')
        self.page_version = Version.objects.create(
            content_type=ContentType.objects.get_for_model(Page),
            object_id=self.page.id,
            template_name='glitter/sample.html',
        )

    def test_html_blocks(self):
        # Add 100 HTML blocks to a page
        html_content_type = ContentType.objects.get_for_model(HTML)

        for block_position in range(1, 101):
            html_block = HTML.objects.create(content='<p>HTML Block</p>')
            content_block = ContentBlock.objects.create(
                obj_version=self.page_version,
                column='main_content',
                position=block_position,
                content_type=html_content_type,
                object_id=html_block.id,
            )
            html_block.content_block = content_block
            html_block.save(update_fields=['content_block'])

        # Two queries:
        # - One to select content blocks, along with their content types
        # - Another to select all HTML blocks
        with self.assertNumQueries(2):
            glitter = Glitter(page_version=self.page_version)
            glitter.render()
