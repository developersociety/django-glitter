# -*- coding: utf-8 -*-

import re

from django.core.exceptions import ValidationError


YOUTUBE_URL_RE = r"""
    (?x)^
    (
        (?:https?://|//)                                     # http(s):// or protocol-independent URL
        (?:(?:(?:(?:\w+\.)?[yY][oO][uU][tT][uU][bB][eE](?:-nocookie)?\.com/|
           youtube\.googleapis\.com/)                        # the various hostnames, with wildcard subdomains
        (?:.*?\#/)?                                          # handle anchor (#/) redirect urls
        (?:                                                  # the various things that can precede the ID:
            (?:(?:v|embed|e)/(?!videoseries))                # v/ or embed/ or e/
            |(?:                                             # or the v= param in all its forms
                (?:(?:watch|movie)(?:_popup)?(?:\.php)?/?)?  # preceding watch(_popup|.php) or nothing (like /?v=xxxx)
                (?:\?|\#!?)                                  # the params delimiter ? or # or #!
                (?:.*?&)??                                   # any other preceding param (like /?s=tuff&v=xxxx)
                v=
            )
        ))
        |(?:www\.)?cleanvideosearch\.com/media/action/yt/watch\?videoId=
        )
    )?                                                       # all until now is optional -> you can pass the naked ID
    ([0-9A-Za-z_-]{11})                                      # here is it! the YouTube video ID
    (?!.*?&list=)                                            # combined list/video URLs are handled by the playlist IE
    (?(1).+)?                                                # if we found the ID, everything can follow
    $
"""  # noqa

VIMEO_URL_RE = r"""
    (?x)
    https?://
    (?:(?:www|(?P<player>player))\.)?
    vimeo(?P<pro>pro)?\.com/
    (?!channels/[^/?#]+/?(?:$|[?#])|album/)
    (?:.*?/)?
    (?:(?:play_redirect_hls|moogaloop\.swf)\?clip_id=)?
    (?:videos?/)?
    (?P<id>[0-9]+)
    /?(?:[?&].*)?(?:[#].*)?$
"""


def validate_url(value):
    """ Validate url. """
    if not re.match(VIMEO_URL_RE, value) and not re.match(YOUTUBE_URL_RE, value):
        raise ValidationError('Invalid URL - only Youtube, Vimeo can be used.')
