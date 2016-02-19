from glitter import block_admin

from .models import HTML


block_admin.site.register(HTML)
block_admin.site.register_block(HTML, 'Common')
