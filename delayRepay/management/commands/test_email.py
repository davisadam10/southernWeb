__author__ = 'adam'


import os
from django.core.management.base import BaseCommand
import delayRepay.models as models
from postmark import PMMail


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = models.UserData.objects.filter(username='davisadam10')[0]
        message = PMMail(
            api_key=os.environ.get('POSTMARK_API_TOKEN'),
            subject="Test",
            sender="admin@southern-fail.co.uk",
            to=str(user.email),
            text_body="Hello",
            tag="testEmail"
        )

        message.send()