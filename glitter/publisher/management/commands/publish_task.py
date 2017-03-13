from __future__ import unicode_literals

from django.core.management.base import BaseCommand

from glitter.publisher.utils import process_actions


class Command(BaseCommand):
    help = 'Process scheduled publishing for Glitter objects'

    requires_system_checks = False

    def handle(self, **options):
        actions_taken = process_actions()
        self.stdout.write('Actions taken: {}'.format(actions_taken))
