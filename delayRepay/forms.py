from django import forms
from models import UserData
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from crispy_forms.bootstrap import FormActions, StrictButton


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
    helper.form_action = '/accounts/auth/'
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-sm-4'
    helper.field_class = 'col-sm-4'
    helper.layout = Layout(
        Field('username', css_class='input-sm'),
        Field('password', css_class='input-sm'),
        Field('remember'),
        FormActions(StrictButton('login', name="login", value="login", css_class="btn-primary")),
        FormActions(StrictButton('register', name="register", value="register", css_class="btn-danger")),
    )