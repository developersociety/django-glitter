from __future__ import unicode_literals

from datetime import timedelta

from django.core.validators import ValidationError
from django.test import SimpleTestCase
from django.utils import timezone

from glitter.publisher.validators import future_date


class TestFutureDateValidator(SimpleTestCase):
    def test_valid_date(self):
        next_week = timezone.now() + timedelta(weeks=1)

        date_valid = future_date(next_week)

        self.assertIsNone(date_valid)

    def test_invalid_past_date(self):
        last_week = timezone.now() - timedelta(weeks=1)

        with self.assertRaises(ValidationError):
            future_date(last_week)
