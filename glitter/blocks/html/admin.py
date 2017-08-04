from glitter.blockadmin import blocks

from .models import HTML


blocks.site.register(HTML)
blocks.site.register_block(HTML, 'Common')
