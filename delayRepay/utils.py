__author__ = 'adam'
import mechanize
import delayRepay.models as models

def get_best_valid_ticket(user, date):
    all_tickets = models.Ticket.objects.filter(delayRepayUser=user)
    validTicket = None
    for ticket in all_tickets:
        if ticket.ticket_start_date <= date <= ticket.ticket_expiry_date:
            if not validTicket:
                validTicket = ticket

            if float(validTicket.cost) < float(ticket.cost):
                validTicket = ticket

    return validTicket


def submit_delay(request, delay, journey, debug=True):
    """

    :param request: the http request passed in
    :type request:
    :param delay: the delay model we are claiming for
    :type delay: models.Delay
    :param journey:
    :type journey: models.Journey
    :param debug:
    :type debug:
    :return:
    :rtype:
    """
    user = models.UserData.objects.filter(username=request.user)[0]
    ticket = get_best_valid_ticket(user, delay.date)
    if not ticket:
        return False

    br = mechanize.Browser()
    url = 'http://www.southernrailway.com/your-journey/customer-services/delay-repay/delay-repay-form'
    br.open(url)

    forms = []

    for form in br.forms():
        forms.append(form)

    main_form = forms[4]
    br.form = list(br.forms())[4]

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

    control = main_form.find_control("uploadedfile_1")
    image_field = ticket.ticket_photo
    image_field.open()
    control.add_file(image_field, 'text/plain', ticket.ticket_photo.name)

    compensation = "National Rail Vouchers"
    main_form['compensation'] = [compensation, ]
    main_form['photocard_id_1'] = user.photocard_id

    if not debug:
        response = br.submit()
        text = response.read()
        return text
        #temp_file = open("/home/adam/temp.html", "w")
        #temp_file.write(text)
        #temp_file.close()

    return True
