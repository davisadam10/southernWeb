__author__ = 'adam'

from django.core.management.base import BaseCommand
import delayRepay.models as models
from datetime import datetime, timedelta



class Command(BaseCommand):
    def handle(self, *args, **options):
        delays = models.Delay.objects.filter(expired=False)
        todays_date = datetime.now().date()
        delayCutoff = datetime.now() + timedelta(-28)
        for delay in delays:
            print delay.date, type(delay.date)
            print delayCutoff, type(delayCutoff)
            if delay.date < delayCutoff:
                delay.expired = True
                delay.delete()
                print 'Expired'