# -*- coding: utf-8 -*-

from django import forms
from django.db.models.fields import BLANK_CHOICE_DASH

from latest_tweets.models import Tweet

from .models import LatestTweetsBlock


class LatestTweetsBlockForm(forms.ModelForm):
    class Meta:
        model = LatestTweetsBlock
        exclude = ()

    user = forms.ChoiceField(required=False)

    def __init__(self, *args, **kwargs):
        super(LatestTweetsBlockForm, self).__init__(*args, **kwargs)

        # To get Tweet objects needs django-latest-tweets should be installed.
        self.fields['user'].choices = BLANK_CHOICE_DASH + [
            (x[0], '@%s - %s' % x) for x in Tweet.objects.order_by(
                'user').distinct().values_list('user', 'name')
        ]
