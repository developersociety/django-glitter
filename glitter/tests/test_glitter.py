from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from glitter.blocks.html.models import HTML
from glitter.models import ContentBlock, Version
from glitter.page import Glitter
from glitter.pages.models import Page


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
