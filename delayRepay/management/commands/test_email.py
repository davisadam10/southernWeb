__author__ = 'adam'



from django.core.management.base import BaseCommand
import delayRepay.models as models
from django.core.mail import send_mail


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = models.UserData.objects.filter(username='davisadam10')[0]
        send_mail(
            'New Delay', 'Hi',
            'admin@southern-fail.co.uk',
            [str(user.email)]
        )