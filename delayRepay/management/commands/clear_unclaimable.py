__author__ = 'adam'
__author__ = 'adam'

from django.core.management.base import BaseCommand
import delayRepay.models as models
import delayRepay.utils as utils
from datetime import datetime

class Command(BaseCommand):
    def handle(self, *args, **options):
        users = models.UserData.objects.all()
        for user in users:
            utils.clear_unclaimable_delays(user)

