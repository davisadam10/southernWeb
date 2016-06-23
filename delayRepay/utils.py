"""
# coding=utf-8
Utils for delay repay
"""
__author__ = 'adam'
from datetime import datetime
from datetime import timedelta
import mechanize
import base64
import delayRepay.models as models
from bs4 import BeautifulSoup
from django.core.files.storage import default_storage as storage
from PIL import Image

DEBUG = False
GLOBAL_BROWSER = {}

def cleanName(name):
    """

    :param name:
    :type name:
    :return:
    :rtype:
    """
    name = name.replace(' ', '_')
    name = name.replace('(', '_')
    name = name.replace(')', '_')
    return name

def create_journey_name(start_station, end_station):
    """

    :param start_station: the name of the station we start at
    :type start_station: str
    :param end_station: the name of the station we end at
    :type end_station:  str
    :return: the name for the journey
    :rtype: str
    """
    return "%s To %s" % (start_station, end_station)


def get_user_journeys(user_data):
    """

    :param user_data: the userData model for the user
    :type user_data: model.UserData
    :return: a list of all the users journeys
    :rtype: list
    """
    return models.Journey.objects.filter(delayRepayUser=user_data).order_by('journeyName')


def get_user_model_from_request(request):
    """

    :param request: the request object from the view
    :type request: django.http.HttpRequest
    :return: the user model from the request supplied
    :rtype: UserData
    """
    if request.user.is_authenticated():
        user_models = models.UserData.objects.filter(username=request.user)
        if user_models:
            return user_models[0]
    return None


def get_best_valid_ticket(user, date):
    """ From all the users tickets, find a valid ticket for the journey date supplied.
        If there are multiple tickets, find the one which cost the most, as to claim
        the maximum back.

    :param user: the user model for current user
    :type user: models.UserData
    :param date: the date of the journey
    :type date: datetime.date
    :return: returns the best ticket if found
    :rtype: Ticket
    """
    all_tickets = models.Ticket.objects.filter(delayRepayUser=user)
    valid_ticket = None
    for ticket in all_tickets:
        if ticket.ticket_start_date <= date <= ticket.ticket_expiry_date:
            if not valid_ticket:
                valid_ticket = ticket

            if float(valid_ticket.cost) < float(ticket.cost):
                valid_ticket = ticket

    return valid_ticket

def get_browser_and_captcha(username):
    """ Get the mechanize browser and captcha image: Note we have to store this in a global variable otherwise
    the captcha does not match

    :return: a tuple of two items, the first is the mechanize browser and the second is the base64 representation of the capture image
    """
    br = mechanize.Browser()
    url = 'http://www.southernrailway.com/your-journey/customer-services/delay-repay/delay-repay-form'
    response = br.open(url)

    global GLOBAL_BROWSER
    print "\n\nSETTING GLOBAL BROWSER"
    GLOBAL_BROWSER[username] = br
    print GLOBAL_BROWSER[username]
    print
    soup = BeautifulSoup(response.get_data(),  "html.parser")
    imgs = soup.find_all('img')
    img = None
    for imgage in imgs:
        if 'CAP' in str(imgage):
            img = imgage

    image_response = br.open_novisit(img['src'])
    im = Image.open(image_response)
    fh = storage.open('captcha.png', "w")
    im.save(fh, 'png')
    fh.close()
    response_data = base64.urlsafe_b64encode(response.read())
    return response_data, storage.url('captcha.png')


def submit_delay(username, delay, journey, encoded_response, answer):
    """

    :param username: the username
    :type username: string
    :param delay: the delay model we are claiming for
    :type delay: models.Delay
    :param journey:
    :type journey: models.Journey
    :param encoded_response: the response which matches the captcha
    :type encoded_response: base64
    :return: if the delay has been successfully submitted
    :rtype: bool
    """
    user = models.UserData.objects.filter(username=username)[0]
    ticket = get_best_valid_ticket(user, delay.date)
    if not ticket:
        return False

    global GLOBAL_BROWSER
    print "\n\nGETTING GLOBAL BROWSER"
    print GLOBAL_BROWSER[username]
    print
    br = GLOBAL_BROWSER[username]

    forms = []

    for form in br.forms():
        forms.append(form)


    formIdx = 4
    main_form = forms[formIdx]
    br.form = list(br.forms())[formIdx]

    main_form['title'] = [user.title, ]
    main_form['forename'] = user.forename
    main_form['surname'] = user.surname
    main_form['email'] = user.email
    main_form['email_confirmation'] = user.email
    main_form['phone'] = user.phoneNum
    main_form['address1'] = user.address1
    main_form['address2'] = user.address2
    main_form['city'] = user.city
    main_form['county'] = user.county
    main_form['postcode'] = user.postcode

    main_form['ticket_type_1'] = [ticket.ticket_type, ]

    pounds, pence = ticket.cost.split('.')
    main_form['cost_pounds_1'] = pounds
    main_form['cost_pence_1'] = pence

    main_form['journey_date_day_1'] = [str(delay.date.day), ]
    main_form['journey_date_month_1'] = [str(delay.date.month).zfill(2), ]
    main_form['journey_date_year_1'] = [str(delay.date.year), ]
    main_form['scheduleddeparturehours_1'] = [str(delay.startTime.hour).zfill(2), ]
    main_form['scheduleddeparturemins_1'] = [str(delay.startTime.minute).zfill(2), ]
    main_form['scheduledarrivalhours_1'] = [str(delay.endTime.hour).zfill(2), ]
    main_form['scheduledarrivalmins_1'] = [str(delay.endTime.minute).zfill(2), ]
    main_form['departing_station_1'] = journey.departingStation
    main_form['arriving_station_1'] = journey.arrivingStation
    main_form['delayReason_1'] = [delay.delay_reason, ]
    main_form['delay_1'] = [delay.delay, ]

    main_form['user_captcha'] = str(answer)

    main_form['photocard_id_1'] = user.photocard_id

    control = main_form.find_control("uploadedfile_1")
    image_field = ticket.ticket_photo
    image_field.open()
    control.add_file(image_field, 'text/plain', ticket.ticket_photo.name)

    main_form['confirmation'] = ['Yes']

    if not DEBUG:
        br.submit()  # returns a response
        #text = response.read()
        #temp_file = open("/Users/adam/temp.html", "w")
        #temp_file.write(text)
        #temp_file.close()

    print '\n\nCLEARING GLOBAL BROWSER'
    GLOBAL_BROWSER[username] = None
    print GLOBAL_BROWSER[username]
    print
    return True


def get_delays_for_date(user_data, date):
    """

    :param user_data: userData model for the user
    :type user_data: models.UserData
    :param date: the date you want to get the users delays for
    :type date: datetime.date
    :return: a list of delays for the given date
    :rtype: list
    """
    return models.Delay.objects.filter(delayRepayUser=user_data, date=date)


def get_delays_for_today(user_data):
    """

    :param user_data: userData model for the user
    :type user_data: models.UserData
    :return: a list of delays for today
    :rtype: list
    """
    return get_delays_for_date(user_data, datetime.now().date())


def get_station_from_name(station_name):
    """

    :param station_name: the name of the station
    :type station_name: string
    :return: the station model object with the name provided
    :rtype: models.Station
    """
    station = None
    stations = models.Station.objects.filter(name=station_name)
    if stations:
        station = stations[0]
    return station


def check_delay_already_found(user, delay_to_check):
    """ Checks to see if the delay provided has already been detected for the given user

    :param user: the user model we want to check
    :type user: models.UserData
    :param delay_to_check: the delay we are checking to see if the user has already found
    :type delay_to_check: models.Delay
    :return: whether or not the delay has been detected for that user
    :rtype: bool
    """
    delays = models.Delay.objects.filter(delayRepayUser=user, date=delay_to_check.date)
    for delay in delays:
        if delay_to_check == delay:
            return True
    return False

def clear_unclaimable_delays(user):
    """

    :param user: the user model we want to check
    :type user: models.UserData
    """
    claimed_delays = models.Delay.objects.filter(claimed=True, delayRepayUser=user)
    claimed_dates = [delay.date for delay in claimed_delays]
    unclaimed_delays = models.Delay.objects.filter(delayRepayUser=user)
    delayCutoff = datetime.now() + timedelta(-28)
    for delay in unclaimed_delays:
        if delay.date in claimed_dates:
            if already_claimed(user, delay.date):
                delay.claimable = False
                delay.delete()
                continue

        if delay.date < delayCutoff:
            delay.delete()

        


def already_claimed(user_model, delay_date, doMaxCheck=False):
    """ Check to see if we have passed the 120 minute maximum delay for the date given

    :param user_model: the user model we want to check
    :type user_model: models.UserData
    :param delay_date: the date we are checking
    :type delay_date: datetime.date
    :param doMaxCheck: whether to check if we have made the 120 min maximum check
    :type doMaxCheck: bool
    :return: whether we have already claimed over our limit or not
    :rtype: bool
    """
    delays = [claimed_delay for claimed_delay in get_delays_for_date(user_model, delay_date) if claimed_delay.claimed]
    if doMaxCheck:
        total = 0

        for delay in delays:
            total += delay.delay_totalizer_value()

        if total < 120:
            return False
        return True
    else:
        if delays:
            return True
        return False
