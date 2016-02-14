from concurrent.futures import ThreadPoolExecutor
from django.core.management.base import BaseCommand
from django.db import connection
from django.db.models import F
from django.utils import timezone

from ww.api.models import Watch

executor = ThreadPoolExecutor(max_workers=5)

class Command(BaseCommand):
    help = 'Sends notifications for new Alarms'

    def _fire_and_mark(self, watch):
        watch.state = 'alarm'
        watch.save()
        watch.fire_flares()
        connection.close()

    def handle(self, *args, **options):
        # We're looking for all currently 'quiet' Watches for which the alarm
        # threshold has been crossed. In other words, we want to find all
        # Watches whose most recent ping was earlier than the duration of
        # (cycle + grace) before now.
        alarm_threshold = timezone.now() - F('cycle') - F('grace')
        quiet = Watch.objects.filter(state = 'quiet')
        new_alarms = quiet.filter(last_ping__lt = alarm_threshold)

        executor.map(self._fire_and_mark, new_alarms)
