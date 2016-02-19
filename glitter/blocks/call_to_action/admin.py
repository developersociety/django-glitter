from glitter import block_admin

from .models import CallToActionBlock


block_admin.site.register(CallToActionBlock)
block_admin.site.register_block(CallToActionBlock, 'Common')
