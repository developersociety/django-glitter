# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from django.db import models

from glitter.models import BaseBlock

from .validators import validate_url, YOUTUBE_URL_RE, VIMEO_URL_RE


class Video(BaseBlock):
    url = models.URLField(
        'URL',
        help_text='YouTube, Vimeo videos only',
        validators=[validate_url],
    )
    html = models.TextField(editable=False)

    class Meta:
        verbose_name = 'video'

    def get_embed_url(self):
        """ Get correct embed url for Youtube or Vimeo. """
        embed_url = None
        youtube_embed_url = 'https://www.youtube.com/embed/{}'
        vimeo_embed_url = 'https://player.vimeo.com/video/{}'

        # Get video ID from url.
        if re.match(YOUTUBE_URL_RE, self.url):
            embed_url = youtube_embed_url.format(re.match(YOUTUBE_URL_RE, self.url).group(2))
        if re.match(VIMEO_URL_RE, self.url):
            embed_url = vimeo_embed_url.format(re.match(VIMEO_URL_RE, self.url).group(3))
        return embed_url

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """ Set html field with correct iframe. """
        if self.url:
            self.html = """<iframe src="{}" frameborder="0" allowfullscreen></iframe>""".format(
                self.get_embed_url()
            )
        return super(Video, self).save(force_insert, force_update, using, update_fields)
