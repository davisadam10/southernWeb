__author__ = 'adam'
__author__ = 'adam'

from django.core.management.base import BaseCommand
import delayRepay.models as models
from datetime import datetime

class Command(BaseCommand):
    def handle(self, *args, **options):
        users = models.UserData.objects.all()
        for user in users:
            claimed_delays = models.Delay.objects.filter(claimed=True, delayRepayUser=user)
            claimed_dates = [delay.date for delay in claimed_delays]
            unclaimed_delays = models.Delay.objects.filter(claimed=False, delayRepayUser=user)
            for delay in unclaimed_delays:
                if delay.date in claimed_dates:
                    delay.claimable = False
                    delay.save()
