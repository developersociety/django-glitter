from django.core.exceptions import ValidationError
from django.core.validators import validate_email, URLValidator
from django.db.models.fields import CharField
from django.forms import URLField, CharField as CharFormField


url_validator = URLValidator()


def valid_mailto(value):
    # Must at least start with mailto
    if not value.lower().startswith('mailto:'):
        return False

    _, email = value.split(':', 1)

    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


def valid_url(value):
    try:
        url_validator(value)
        return True
    except ValidationError:
        return False


def validate_link(value):
    """ Validate if a value is a valid link - either a URL or mailto. """
    if not any([valid_mailto(value), valid_url(value)]):
        raise ValidationError('Enter a valid link')


class LinkField(CharField):
    default_validators = [validate_link]
    description = 'Link'

    def __init__(self, *args, **kwargs):
        # max_length=254 to be compliant with RFCs 3696 and 5321
        kwargs['max_length'] = kwargs.get('max_length', 254)
        super(LinkField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        # As with CharField, this will cause validation to be performed twice.
        defaults = {
            'form_class': LinkFormField,
        }
        defaults.update(kwargs)
        return super(LinkField, self).formfield(**defaults)


class LinkFormField(URLField):
    default_error_messages = {
        'invalid': 'Enter a valid link',
    }
    default_validators = [validate_link]

    def to_python(self, value):
        # Slightly evil - ignore URLField's to_python if we're starting with mailto:
        value = super(CharFormField, self).to_python(value)

        if value and value.lower().startswith('mailto:'):
            return value

        # Go through URLField's to_python
        value = super(LinkFormField, self).to_python(value)

        return value
