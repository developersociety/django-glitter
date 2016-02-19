# -*- coding: utf-8 -*-


class GlitterRedirectException(Exception):
    def __init__(self, url):
        self.url = url

    def __str__(self):
        return 'Redirect to %s required' % (self.url,)


class GlitterUnpublishedException(Exception):
    def __init__(self, obj):
        self.obj = obj

    def __str__(self):
        return '%s is not published' % (self.obj,)
