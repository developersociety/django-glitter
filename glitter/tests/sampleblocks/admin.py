from glitter.blockadmin import blocks

from .models import SampleModelWithInlinesBlock, SampleInline


class SampleInlineAdmin(blocks.StackedInline):
    model = SampleInline


class SampleModelWithInlinesBlockAdmin(blocks.BlockAdmin):
    inlines = [SampleInlineAdmin]


blocks.site.register(SampleModelWithInlinesBlock, SampleModelWithInlinesBlockAdmin)
blocks.site.register_block(SampleModelWithInlinesBlock, 'Sample Blocks')
