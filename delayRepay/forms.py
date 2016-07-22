# coding=utf-8
"""
Module which contains all of the forms for the site
"""
from django import forms
from models import UserData, Journey, Ticket, Delay, Station
import utils as utils
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from crispy_forms.bootstrap import FormActions
import datetime
from django.core.mail import send_mail


class DelayRepayUserRegForm(UserCreationForm):
    """
    Form for a user to register their details for the site
    """
    email = forms.EmailField(required=True)

    title_choices = [("Mr", "Mr"), ("Mrs", "Mrs"), ("Miss", "Miss"), ("Ms", "Ms")]
    title = forms.ChoiceField(choices=title_choices)

    forename = forms.CharField(required=True)
    surname = forms.CharField(required=True)
    phoneNum = forms.IntegerField(required=True)

    address1 = forms.CharField(required=True)
    address2 = forms.CharField(required=True)
    city = forms.CharField(required=True)
    county = forms.CharField(required=True)
    postcode = forms.CharField(required=True, max_length=7, min_length=6)
    photocard_id = forms.CharField(required=True, max_length=7, min_length=7)

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-sm-4'
    helper.field_class = 'col-sm-4'
    helper.layout = Layout(
        Field('username', css_class='input-sm'),
        Field('password1', css_class='input-sm'),
        Field('password2', css_class='input-sm'),
        Field('title', css_class='input-sm'),
        Field('forename', css_class='input-sm'),
        Field('surname', css_class='input-sm'),
        Field('email', css_class='input-sm'),
        Field('phoneNum', css_class='input-sm'),
        Field('address1', css_class='input-sm'),
        Field('address2', css_class='input-sm'),
        Field('city', css_class='input-sm'),
        Field('county', css_class='input-sm'),
        Field('postcode', css_class='input-sm'),
        Field('photocard_id', css_class='input-sm'),
        FormActions(Submit('Register', 'Register', css_class='btn-primary'))
    )

    class Meta(object):
        model = UserData
        fields = (
            "username", "email",
            "password1", "password2",
            "title", "forename", "surname",
            "phoneNum", "address1", "address2",
            "city", "county", "postcode", "photocard_id"
        )

    def save(self, commit=True):
        user = super(DelayRepayUserRegForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.title = self.cleaned_data['title']
        user.forename = self.cleaned_data['forename']
        user.surname = self.cleaned_data['surname']
        user.phoneNum = self.cleaned_data['phoneNum']
        user.address1 = self.cleaned_data['address1']
        user.address2 = self.cleaned_data['address2']
        user.city = self.cleaned_data['city']
        user.county = self.cleaned_data['county']
        user.postcode = self.cleaned_data['postcode']
        user.photocard_id = self.cleaned_data['photocard_id']
        user.is_active = False
        if commit:
            user.save()
            send_mail(
                'Welcome!', 'Hi %s,\n\nYour application has been received please allow 24 hours for activation\n\nwww.southern-fail.co.uk\n\n' % user.forename,
                'admin@southern-fail.co.uk',
                [str(user.email)]
            )

        return user


class LoginForm(forms.Form):
    username = forms.CharField(label="Username", required=True)
    password = forms.CharField(
        label="Password", required=True, widget=forms.PasswordInput)
    remember = forms.BooleanField(label="Remember Me?", required=False)

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_action = '/login/'
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-sm-4'
    helper.field_class = 'col-sm-4'
    helper.layout = Layout(
        Field('username', css_class='input-sm'),
        Field('password', css_class='input-sm'),
        Field('remember'),
        FormActions(Submit('login',  value="login", css_class="btn-primary")),
        FormActions(Submit('register', value="register", css_class="btn-danger")),
    )


class AnswerCaptchaForm(forms.Form):
    imageUrl = forms.CharField(label='imageUrl')
    encoded_response = forms.CharField(label='encoded_response')
    answer = forms.CharField(label='answer')
    username = forms.CharField(label='username')
    delayId = forms.CharField(label='delayId')
    journeyId = forms.CharField(label='journeyId')

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_action = '/answerCaptcha/'
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-sm-4'
    helper.field_class = 'col-sm-4'
    helper.layout = Layout(
        Field('imageUrl', css_class='input-sm', type="hidden"),
        Field('encoded_response', css_class='input-sm', type="hidden"),
        Field('answer', css_class='input-sm'),
        Field('username', css_class='input-sm', type="hidden"),
        Field('delayId', css_class='input-sm', type="hidden"),
        Field('journeyId', css_class='input-sm', type="hidden"),
        FormActions(Submit('submit',  value="submit", css_class="btn-primary")),
    )

    def clean(self):
        cleaned_data = super(AnswerCaptchaForm, self).clean()
        msg = "Captcha answer must be 5 characters long"
        if "answer" in cleaned_data:
            if len(cleaned_data['answer']) != 5:
                raise forms.ValidationError(
                    msg
                )


class DelayForm(forms.ModelForm):
    delays = [
        ('30-59 mins', '30-59 mins'),
        ('60-119 mins', '60-119 mins'),
        ('120+ mins', '120+ mins')
    ]

    delay_reasons = [
        ('Train cancelled', 'Train cancelled'),
        ('Delayed on route', 'Delayed on route'),
        ('Delayed departure', 'Delayed departure'),
        ('Missed connection', 'Missed connection'),
        ('Other', 'Other')
    ]

    def __init__(self, *args, **kwargs):
            super(DelayForm, self).__init__(*args, **kwargs)
            self.fields['journey_date'].widget.format = '%d/%m/%Y'

            # at the same time, set the input format on the date field like you want it:
            self.fields['journey_date'].input_formats = ['%d/%m/%Y']

    delay = forms.ChoiceField(choices=delays)
    delay_reason = forms.ChoiceField(choices=delay_reasons)

    journey_name = forms.CharField(required=True)
    journey_date = forms.DateField()
    start_time = forms.TimeField()
    end_time = forms.TimeField()
    delay_details = forms.CharField(required=False)

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_action = '/'
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-sm-4'
    helper.field_class = 'col-sm-4'
    helper.layout = Layout(
        Field('delay', css_class='input-sm'),
        Field('delay_reason', css_class='input-sm'),
        Field('journey_name', css_class='input-sm', type="hidden"),
        Field('journey_date', css_class='datepicker', id='datepicker'),
        Field('start_time', css_class='input-sm', id='timepicker'),
        Field('end_time', css_class='input-sm', id='timepicker2'),
        Field('delay_details', css_class='input-sm'),
        FormActions(Submit('Submit Delay', 'Submit Delay', css_class='btn-primary')),
    )

    class Meta(object):
        model = Delay
        fields = ("delay", "delay_reason", "journey_date", "start_time", "end_time")

    def save(self, commit=True, user=None, journey=None):
        delay = super(DelayForm, self).save(commit=False)
        delay.delay = self.cleaned_data['delay']
        delay.delay_reason = self.cleaned_data['delay_reason']
        delay.date = self.cleaned_data['journey_date']
        delay.startTime = self.cleaned_data['start_time']
        delay.endTime = self.cleaned_data['end_time']
        delay.journey = journey
        delay.delay_details = self.cleaned_data['delay_details']
        user_models = UserData.objects.filter(username=user)
        delay.delayRepayUser = user_models[0]
        if commit:
            delay.save()

        return delay

    def clean(self):
        cleaned_data = super(DelayForm, self).clean()
        msg = "Please select a journey or add a journey"
        if "journey_name" in cleaned_data:
            if cleaned_data['journey_name'] == "":
                raise forms.ValidationError(
                    msg
                )
        else:
            raise forms.ValidationError(
                    msg
                )


class JourneyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(JourneyForm, self).__init__(*args, **kwargs)

    all_stations = Station.objects.all()
    validStations = [(station.name, station.name)for station in all_stations]
    validStations.sort()

    departing_station = forms.ChoiceField(choices=validStations)
    arriving_station = forms.ChoiceField(choices=validStations)

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_action = '/addJourney/'
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-sm-4'
    helper.field_class = 'col-sm-4'
    helper.layout = Layout(
        Field('departing_station'),
        Field('arriving_station'),
        FormActions(Submit('Add Journey', 'Add Journey', css_class='btn-primary'))
    )

    class Meta(object):
        model = Journey
        fields = ("departing_station", "arriving_station")

    def save(self, commit=True):
        journey = super(JourneyForm, self).save(commit=False)
        journey.journeyName = utils.create_journey_name(
            self.cleaned_data['departing_station'],
            self.cleaned_data['arriving_station']
        )
        journey.departingStation = self.cleaned_data['departing_station']
        journey.arrivingStation = self.cleaned_data['arriving_station']
        user_model = utils.get_user_model_from_request(self.request)
        journey.delayRepayUser = user_model
        if commit:
            journey.save()

        return journey

    def clean(self):
        cleaned_data = super(JourneyForm, self).clean()
        if cleaned_data['departing_station'] == self.cleaned_data['arriving_station']:
            msg = "Journey can not begin and end at the same station"
            self.add_error('departing_station', msg)
            self.add_error('arriving_station', msg)
            raise forms.ValidationError(
                msg
            )

        journey_name = utils.create_journey_name(cleaned_data['departing_station'], self.cleaned_data['arriving_station'])
        user_model = utils.get_user_model_from_request(self.request)
        journey_names = [journey.journeyName for journey in utils.get_user_journeys(user_model)]
        if journey_name in journey_names:
            raise forms.ValidationError(
                "This journey is already added to your common journeys"
            )

class FriendForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(FriendForm, self).__init__(*args, **kwargs)

    friend_email = forms.EmailField()

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_action = '/addFriend/'
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-sm-4'
    helper.field_class = 'col-sm-4'
    helper.layout = Layout(
        Field('friend_email', id='id_friend_email'),
        FormActions(Submit('Add Friend', 'Add Friend', css_class='btn-primary'))
    )

    class Meta(object):
        fields = ("friend_email")

    def clean(self):
        cleaned_data = super(FriendForm, self).clean()
        my_user = utils.get_user_model_from_request(self.request)
        if my_user.email == cleaned_data['friend_email']:
            msg = "Cant add your own email address as a friend"
            raise forms.ValidationError(
                msg
            )

        already_friends = [friend.email for friend in my_user.friends.all()]
        if cleaned_data['friend_email'] in already_friends:
            msg = "This person is already your friend"
            raise forms.ValidationError(
                msg
            )

        users = UserData.objects.filter(email=cleaned_data['friend_email'])
        if not users:
            msg = "No users matching email address provided found"
            raise forms.ValidationError(
                msg
            )
        else:
            cleaned_data['friend_model'] = users[0]

        return cleaned_data

class TicketForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
            super(TicketForm, self).__init__(*args, **kwargs)
            self.fields['ticket_start_date'].widget.format = '%d/%m/%Y'

            # at the same time, set the input format on the date field like you want it:
            self.fields['ticket_start_date'].input_formats = ['%d/%m/%Y']

            self.fields['ticket_expiry_date'].widget.format = '%d/%m/%Y'

            # at the same time, set the input format on the date field like you want it:
            self.fields['ticket_expiry_date'].input_formats = ['%d/%m/%Y']

    valid_ticket_types = (
        ("weekly", 'weekly'),
        ("monthly", 'monthly'),
        ("yearly", 'yearly'),


    )

    ticket_type = forms.ChoiceField(choices=valid_ticket_types)
    cost = forms.CharField(required=True)
    ticketNumPart1 = forms.CharField(required=True, max_length=5, min_length=5)
    ticketNumPart2 = forms.CharField(required=True, max_length=10, min_length=10)
    ticket_start_date = forms.DateField(required=True)
    ticket_expiry_date = forms.DateField(required=True)
    ticket_photo = forms.ImageField(required=True)

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_action = '/addTicket/'
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-sm-4'
    helper.field_class = 'col-sm-4'
    helper.layout = Layout(
        Field('ticket_type'),
        Field('cost'),
        Field('ticketNumPart1'),
        Field('ticketNumPart2'),
        Field('ticket_start_date', css_class='datepicker', id='datepicker'),
        Field('ticket_expiry_date', css_class='datepicker', id='datepicker2'),
        Field('ticket_photo'),
        FormActions(Submit('Add Ticket', 'Add Ticket', css_class='btn-primary'))
    )

    class Meta(object):
        model = Ticket
        fields = ('ticket_type', 'cost', 'ticket_start_date', 'ticket_expiry_date', 'ticket_photo')

    def save(self, commit=True, user=None):
        ticket = super(TicketForm, self).save(commit=False)
        ticket.ticket_type = self.cleaned_data['ticket_type']
        ticket.cost = self.cleaned_data['cost']
        ticket.ticketNumPart1 = self.cleaned_data['ticketNumPart1']
        ticket.ticketNumPart2 = self.cleaned_data['ticketNumPart2']
        ticket.ticket_start_date = self.cleaned_data['ticket_start_date']
        ticket.ticket_expiry_date = self.cleaned_data['ticket_expiry_date']
        user_models = UserData.objects.filter(username=user)
        ticket.delayRepayUser = user_models[0]
        date_str_format = "%Y_%m_%d_%H_%M_%S"
        in_memory_field = self.cleaned_data['ticket_photo']
        in_memory_field.name = '%s_%s_%s.jpg' % (
            ticket.delayRepayUser.forename,
            ticket.delayRepayUser.surname,
            datetime.datetime.now().strftime(date_str_format)
        )
        ticket.ticket_photo = in_memory_field
        if commit:
            ticket.save()

        return ticket