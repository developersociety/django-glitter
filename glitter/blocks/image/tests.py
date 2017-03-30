# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.test import TestCase

from glitter.blockadmin.blocks import BlockAdminSite


class TestImageBlockAdmin(TestCase):
    fixtures = ['image.json']

    def setUp(self):
        self.site = BlockAdminSite(name='block_admin')

    def test_lazy_loading(self):
        url = reverse('block_admin:get-lazy-images')

        # Test if throws the errors without passing any arguments
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)

        # Test by passing the string for the `last_image_image`
        response = self.client.get(url, {'last_image_id': 'test'})
        self.assertEqual(response.status_code, 400)

        # Test to see if gets the image if the id passed is higher then the one available.
        response = self.client.get(url, {'last_image_id': 2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(1, len(response.context['images']))
