# -*- coding: utf-8 -*-

from glitter import block_admin

from .models import ContactFormBlock


block_admin.site.register(ContactFormBlock)
block_admin.site.register_block(ContactFormBlock, 'Forms')
