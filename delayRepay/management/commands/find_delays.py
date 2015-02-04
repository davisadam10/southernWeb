__author__ = 'adam'

from datetime import datetime
from django.core.management.base import BaseCommand
import delayRepay.models as models
import delayRepay.utils as utils
import delayRepay.nationalRailUtils as nationalRailUtils


class Command(BaseCommand):
    def handle(self, *args, **options):

        users = models.UserData.objects.all()
        for user in users:
            delay_found = None
            already_claimed_today = None
            journeys = utils.get_user_journeys(user)
            count = 0
            for journey in journeys:
                if not delay_found:
                    arriving_station = utils.get_station_from_name(journey.arrivingStation)
                    departing_station = utils.get_station_from_name(journey.departingStation)

                    services = nationalRailUtils.get_services_from_to(
                        departing_station.short_name,
                        arriving_station.short_name
                    )
                    for service in services:
                        cancelled = nationalRailUtils.is_service_cancelled(service)
                        # Should be cancelled but for debugging I have more info
                        if cancelled:
                            hour, minute = service.std.split(':')
                            service_origin = service.origin.location[0].locationName
                            if journey.departingStation != service_origin:
                                print "%s Found A Cancelled Train To %s calling at %s starting from %s @ %s:%s" % (
                                    user.forename,
                                    journey.arrivingStation,
                                    journey.departingStation,
                                    service_origin,
                                    hour,
                                    minute
                                )
                            else:
                                # Easy As departing station is end of the line so no problems
                                print "%s Found A Cancelled Train To %s calling at %s starting from %s @ %s:%s" % (
                                    user.forename,
                                    journey.arrivingStation,
                                    journey.departingStation,
                                    service_origin,
                                    hour,
                                    minute
                                )
                                #print service
                                #nationalRailUtils.findServiceArrival(arriving_station.short_name, service.serviceID)

                                '''
                                newDelay = models.Delay()
                                newDelay.delayRepayUser(user)
                                newDelay.journey(journey)
                                newDelay.date = datetime.now().date()
                                '''



