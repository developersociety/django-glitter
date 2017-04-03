from django.core.validators import ValidationError
from django.utils import timezone


def future_date(date):
    """
    Validator which only allows current/future datetimes.
    """
    if date < timezone.now():
        raise ValidationError("Can't set a scheduled time in the past")
