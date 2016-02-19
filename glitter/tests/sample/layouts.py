# -*- coding: utf-8 -*-

from glitter import columns, templates
from glitter.layouts import PageLayout
from glitter.pages.models import Page


class SampleLayout(PageLayout):
    main_content = columns.Column(width=960)
    side = columns.Column(width=320)

    class Meta:
        template = 'glitter/sample.html'
        verbose_name = 'Sample'


class Sample2Layout(PageLayout):
    content = columns.Column(width=480)
    side = columns.Column(width=320)
    rside = columns.Column(width=320)

    class Meta:
        template = 'glitter/sample2.html'
        verbose_name = 'Sample2'


templates.register(SampleLayout, Page)
templates.register(Sample2Layout, 'glitter_pages.Page')
