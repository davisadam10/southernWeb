__author__ = 'adam'

from django.core.management.base import BaseCommand
import delayRepay.models as models
from datetime import datetime, timedelta



class Command(BaseCommand):
    def handle(self, *args, **options):
        delays = models.Delay.objects.all()
        delayCutoff = datetime.now().date() + timedelta(-28)
        for delay in delays:
            if delay.date < delayCutoff:
                delay.delete()
                