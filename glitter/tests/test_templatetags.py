from __future__ import unicode_literals

try:
    from unittest import mock
except ImportError:
    import mock

from django.template import Context, Template
from django.test import SimpleTestCase

from glitter.templatetags.glitter import glitter_head, glitter_startbody


class TestGlitterHead(SimpleTestCase):
    def test_anonymous_user(self):
        context = Context()

        html = glitter_head(context=context)

        self.assertEqual(html, '')

    def test_staff_user(self):
        user = mock.Mock(is_staff=True)
        context = Context({
            'user': user,
        })
        context.template = mock.Mock()
        context.template.engine.get_template.return_value = Template('<p>Staff User</p>')

        html = glitter_head(context=context)

        context.template.engine.get_template.assert_called_once_with('glitter/include/head.html')
        self.assertEqual(html, '<p>Staff User</p>')


class TestGlitterStartbody(SimpleTestCase):
    def test_anonymous_user(self):
        context = Context()

        html = glitter_startbody(context=context)

        self.assertEqual(html, '')

    def test_no_glitter_object(self):
        user = mock.Mock(is_staff=True)
        context = Context({
            'user': user,
        })
        context.template = mock.Mock()
        context.template.engine.select_template.return_value = Template('<p>Staff User</p>')

        html = glitter_startbody(context=context)

        context.template.engine.select_template.assert_called_once_with(
            ['glitter/include/startbody.html']
        )
        self.assertEqual(html, '<p>Staff User</p>')

    def test_glitter_object(self):
        user = mock.Mock(is_staff=True)
        glitter = mock.Mock()
        glitter.obj._meta.app_label = 'applabel'
        glitter.obj._meta.model_name = 'modelname'
        context = Context({
            'user': user,
            'glitter': glitter,
        })
        context.template = mock.Mock()
        context.template.engine.select_template.return_value = Template('<p>Staff User</p>')

        html = glitter_startbody(context=context)

        context.template.engine.select_template.assert_called_once_with([
            'glitter/include/startbody_applabel_modelname.html',
            'glitter/include/startbody.html',
        ])
        self.assertEqual(html, '<p>Staff User</p>')
