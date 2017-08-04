from glitter.blockadmin import blocks

from .models import ContactFormBlock


blocks.site.register(ContactFormBlock)
blocks.site.register_block(ContactFormBlock, 'Forms')
