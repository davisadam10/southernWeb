from django import forms
from models import UserData, Journey, Ticket
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from crispy_forms.bootstrap import FormActions


class DelayRepayUserRegForm(UserCreationForm):
    email = forms.EmailField(required=True)

    title_choices = [("Mr", "Mr"), ("Mrs", "Mrs"), ("Miss", "Miss"), ("Ms", "Ms")]
    title = forms.ChoiceField(choices=title_choices, required=True)

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

    class Meta:
        model = UserData

        fields = ("username", "email",
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
        if commit:
            user.save()

        return user

class LoginForm(forms.Form):
    username = forms.CharField(label="Username", required=True)
    password = forms.CharField(
        label="Password", required=True, widget=forms.PasswordInput)
    remember = forms.BooleanField(label="Remember Me?")

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_action = 'auth/'
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

class JourneyForm(forms.ModelForm):
    validStations = (
        ("1", "Earlswood (Surrey)"),
        ("2", "Merstham"),
        ("3", "London Victoria"),
        ("4", "London Bridge"),
        ("5", "East Croydon"),
    )

    departing_station = forms.ChoiceField(choices=validStations, required=True)
    arriving_station = forms.ChoiceField(choices=validStations, required=True)
    journey_date = forms.DateField()
    start_time = forms.TimeField()
    end_time = forms.TimeField()


    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_action = '/addJourney/'
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-sm-4'
    helper.field_class = 'col-sm-4'
    helper.layout = Layout(
        Field('departing_station'),
        Field('arriving_station'),
        Field('journey_date', css_class='datepicker', id='datepicker'),
        Field('start_time', css_class='input-sm', id='timepicker'),
        Field('end_time', css_class='input-sm', id='timepicker2'),
        FormActions(Submit('Add Journey', 'Add Journey', css_class='btn-primary'))
    )

    class Meta:
        model = Journey

        fields = ("departing_station", "arriving_station",
                  "journey_date", "start_time",
                  "end_time"
        )

    def save(self, commit=True):
        journey = super(JourneyForm, self).save(commit=False)
        journey.departingStation = self.cleaned_data['departing_station']
        journey.arrivingStation = self.cleaned_data['arriving_station']
        journey.date = self.cleaned_data['journey_date']
        journey.startTime = self.cleaned_data['start_time']
        journey.endTime = self.cleaned_data['end_time']
        if commit:
            pass
            #journey.save()

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

class TicketForm(forms.ModelForm):
    valid_ticket_types = (
        ("1", 'monthly'),
        ("1", 'yearly'),
    )

    ticket_type = forms.ChoiceField(choices=valid_ticket_types, required=True)
    cost = forms.CharField(required=True)
    ticket_start_date = forms.DateField()
    ticket_expiry_date = forms.DateField()

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_action = '/submit/'
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-sm-4'
    helper.field_class = 'col-sm-4'
    helper.layout = Layout(
        Field('ticket_type'),
        Field('cost'),
        Field('ticket_start_date', css_class='datepicker', id='datepicker'),
        Field('ticket_expiry_date', css_class='datepicker', id='datepicker2'),
    )

    class Meta:
        model = Ticket

        fields = ("ticket_type", "cost",
                  "ticket_start_date",
                  "ticket_expiry_date"
        )

    def save(self, commit=True):
        ticket = super(TicketForm, self).save(commit=False)
        ticket.ticket_type = self.cleaned_data['ticket_type']
        ticket.cost = self.cleaned_data['cost']
        ticket.ticket_start_date = self.cleaned_data['ticket_start_date']
        ticket.ticket_expiry_date = self.cleaned_data['ticket_expiry_date']
        if commit:
            ticket.save()

        return ticket