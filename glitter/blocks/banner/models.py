from django.db import models

from glitter.assets.fields import AssetForeignKey
from glitter.fields import LinkField
from glitter.models import BaseBlock


class Banner(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    image = AssetForeignKey('glitter_assets.Image', null=True, blank=True)
    description = models.TextField(blank=True)
    link = LinkField(blank=True)
    link_text = models.CharField(max_length=100, blank=True)
    new_window = models.BooleanField('Open link in new window', default=False)

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title


class BannerBlock(BaseBlock):
    render_function = 'glitter.blocks.banner.views.banner_view'

    class Meta:
        verbose_name = 'banner'


class BannerInline(models.Model):
    banner_block = models.ForeignKey(BannerBlock)
    banner = models.ForeignKey(Banner, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'banner'
        ordering = ('id',)

    def __str__(self):
        return '%s' % (self.banner,) or 'Banner'
