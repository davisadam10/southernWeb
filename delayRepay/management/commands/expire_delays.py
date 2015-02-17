__author__ = 'adam'

from django.core.management.base import BaseCommand
import delayRepay.models as models
from datetime import datetime


class Command(BaseCommand):
    def handle(self, *args, **options):
        delays = models.Delay.objects.filter(expired=False)
        todays_date = datetime.now().date()
        for delay in delays:
            if (todays_date - delay.date).days > 28:
                delay.expired = True
                delay.save()
                print 'Expired'