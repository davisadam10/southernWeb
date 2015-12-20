__author__ = 'adam'

from datetime import datetime, time
from django.core.management.base import BaseCommand
import delayRepay.models as models
import delayRepay.utils as utils
import delayRepay.nationalRailUtils as nationalRailUtils
from django.core.mail import send_mail


class Command(BaseCommand):
    def handle(self, *args, **options):
        time_now = datetime.now().time()
        train_end_time = time(23, 59)
        train_start_time = time(5, 00)

        if not train_end_time > time_now > train_start_time:
            print 'Trains have stopped running'
            return
        else:
            print 'Trains are running checking for delays'
        users = models.UserData.objects.all()
        for user in users:
            delay_found_depart = False
            delay_found_arrive = False
            delay_found = delay_found_depart and delay_found_arrive

            already_claimed_today = utils.already_claimed(user, datetime.now().date())
            journeys = utils.get_user_journeys(user)
            if already_claimed_today:
                print "%s Has Already Made A Claim Today" % user.forename
            for journey in journeys:
                if not delay_found and not already_claimed_today:
                    arriving_station = utils.get_station_from_name(journey.arrivingStation)
                    departing_station = utils.get_station_from_name(journey.departingStation)

                    services = nationalRailUtils.get_services_from_to(
                        departing_station.short_name,
                        arriving_station.short_name
                    )

                    services2 = nationalRailUtils.get_services_arriving_from(
                        departing_station.short_name,
                        arriving_station.short_name
                    )

                    all_services = services + services2
                    for service in all_services:
                        cancelled = nationalRailUtils.is_service_cancelled(service)
                        # Should be cancelled but for debugging I have more info
                        if cancelled:
                            arrival = False
                            if 'sta' in service:
                                hour, minute = service.sta.split(':')
                                arrival = True
                            else:
                                hour, minute = service.std.split(':')

                            service_origin = service.origin.location[0].locationName
                            if journey.departingStation != service_origin:
                                print "Harder as start station is not the beginning of the line"
                                print "%s Found A Cancelled Train To %s calling at %s starting from %s @ %s:%s" % (
                                    user.forename,
                                    journey.arrivingStation,
                                    journey.departingStation,
                                    service_origin,
                                    hour,
                                    minute
                                )

                                station = models.Station.objects.filter(name=journey.arrivingStation)[0]
                                serviceArrival = nationalRailUtils.findServiceArrivalTime(service_origin, "%s:%s" % (hour, minute), station.short_name, service.serviceID, journey.departingStation)
                                if serviceArrival:
                                    arrivalHour, arrivalMinute = serviceArrival.split(':')

                                    newDelay = models.Delay()
                                    newDelay.startTime = time(int(hour), int(minute))
                                    newDelay.endTime = time(int(arrivalHour), int(arrivalMinute))
                                    newDelay.delay = '30-59 mins'
                                    newDelay.delay_reason = 'Train cancelled'
                                    newDelay.delayRepayUser = user
                                    newDelay.journey = journey
                                    newDelay.date = datetime.now().date()

                                    if not utils.check_delay_already_found(user, newDelay):
                                        newDelay.save()
                                        delay_found_arrive = True
                                        send_mail(
                                                'New Delay',
                                                'Hi %s,\n\nA delay has been detected and added to your account\n\nClaim at www.southern-fail.co.uk\n\n%s' % (
                                                user.forename, newDelay),
                                                'admin@southern-fail.co.uk',
                                                [str(user.email)]
                                        )

                                        friends = user.friends.all()
                                        for friend in friends:
                                            delays_on_date = utils.get_delays_for_date(friend, newDelay.date)
                                            if not delays_on_date:
                                                newDelay.claimed = False
                                                newDelay.pk = None
                                                newDelay.delayRepayUser = friend
                                                if not utils.check_delay_already_found(friend, newDelay):
                                                    newDelay.save()
                                                    send_mail(
                                                            'New Delay',
                                                            'Hi %s,\n\nA delay has been detected and added to your account\n\nClaim at www.southern-fail.co.uk\n\n%s' % (
                                                            user.forename, newDelay),
                                                            'admin@southern-fail.co.uk',
                                                            [str(friend.email)]
                                                    )
                                                else:
                                                    print 'Delay Already Detected For %s' % friend.forename
                                    print 'Delay Already Detected For %s' % user.forename


                            else:
                                print "Easy As departing station is end of the line so no problems"
                                extra = ''
                                if arrival:
                                    extra = ' Arriving '

                                print "%s Found A Cancelled Train To %s calling at %s starting from %s %s @ %s:%s" % (
                                    user.forename,
                                    journey.arrivingStation,
                                    journey.departingStation,
                                    service_origin,
                                    extra,
                                    hour,
                                    minute
                                )
                                if arrival:
                                    departure_details = nationalRailUtils.getServiceDepartDetails(service.serviceID)
                                    newDelay = models.Delay()
                                    newDelay.startTime = departure_details['startTime']
                                    newDelay.endTime = time(int(hour), int(minute))
                                    newDelay.delay = '30-59 mins'
                                    newDelay.delay_reason = 'Train cancelled'
                                    newDelay.delayRepayUser = user
                                    newDelay.journey = journey
                                    newDelay.date = datetime.now().date()
                                    if not utils.check_delay_already_found(user, newDelay):
                                        newDelay.save()
                                        delay_found_depart = True
                                        send_mail(
                                            'New Delay', 'Hi %s,\n\nA delay has been detected and added to your account\n\nClaim at www.southern-fail.co.uk\n\n%s' % (user.forename, newDelay),
                                            'admin@southern-fail.co.uk',
                                            [str(user.email)]
                                        )

                                        friends = user.friends.all()
                                        for friend in friends:
                                            delays_on_date = utils.get_delays_for_date(friend, newDelay.date)
                                            if not delays_on_date:
                                                newDelay.claimed = False
                                                newDelay.pk = None
                                                newDelay.delayRepayUser = friend
                                                if not utils.check_delay_already_found(friend, newDelay):
                                                    newDelay.save()
                                                    send_mail(
                                                        'New Delay', 'Hi %s,\n\nA delay has been detected and added to your account\n\nClaim at www.southern-fail.co.uk\n\n%s' % (user.forename, newDelay),
                                                        'admin@southern-fail.co.uk',
                                                        [str(friend.email)]
                                                    )
                                                else:
                                                    print 'Delay Already Detected For %s' % friend.forename
                                    print 'Delay Already Detected For %s' % user.forename

                delay_found = delay_found_arrive and delay_found_depart
            if not already_claimed_today:
                if not delay_found:
                    print 'No Cancelled Trains Found For %s' % user.forename










