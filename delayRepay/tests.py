"""
coding=utf-8
Unit tests and functional tests for delay repay
"""

import time
import datetime


chromedriver = "/usr/bin/chromedriver"
from selenium import webdriver
from django.test import TestCase, LiveServerTestCase
from delayRepay.models import UserData, Station, Journey, Delay, Ticket
import delayRepay.utils as utils
from django.core.files.uploadedfile import SimpleUploadedFile

# Turn The debugging on so that we don't submit any delays during unit testing
utils.DEBUG = True

TEARDOWN_TIME = 0

def wait(amount=None):
    if amount:
        time.sleep(amount)
    time.sleep(0.5)

class BaseDelayRepayTesting(TestCase):
    testUsers = ['Adam', 'Holly', 'Kelly', 'Ben']
    test_stations = ['Earlswood (Surrey)', 'London Victoria']
    password = 'testing'

    def setUp(self):
        for name in self.testUsers:
            user = UserData()
            user.title = 'Mr'
            user.first_name = "%s" % name
            user.username = "User_%s" % name
            user.email = "%s@%s.com" % (user.first_name, user.first_name)
            user.set_password('testing')
            user.save()

            journey = Journey()
            journey.journeyName = utils.create_journey_name(self.test_stations[0], self.test_stations[1])
            journey.arrivingStation = self.test_stations[0]
            journey.departingStation = self.test_stations[1]
            journey.delayRepayUser = user
            journey.save()

            today = datetime.datetime.now().date()
            ticket = Ticket()
            ticket.cost = 330.00
            ticket.ticket_start_date = datetime.datetime(today.year, today.month -1, today.day)
            ticket.ticket_expiry_date = datetime.datetime(today.year, today.month + 1, today.day)
            ticket.delayRepayUser = user
            ticket.ticket_photo = SimpleUploadedFile('best_file_eva.txt', 'these are the file contents!')
            ticket.save()

            for count in xrange(0, 10):
                delay = Delay()
                date = datetime.datetime.now().date()
                if count % 2 == 0:
                    delay.date = date
                else:
                    delay.date = datetime.datetime(date.year+1, date.month+1, date.day+1).date()
                delay.startTime = datetime.datetime.now().time()
                delay.endTime = datetime.datetime.now().time()
                delay.delay = '30-59 mins'
                delay.delay_reason = 'Train cancelled'
                delay.delayRepayUser = user
                claimed = False
                if count % 2 != 0:
                    claimed = True
                delay.claimed = claimed
                delay.journey = journey
                delay.save()

        for station_name in self.test_stations:
            station = Station()
            station.name = station_name
            station.save()


# Create your tests here.
class UserModelTests(BaseDelayRepayTesting):
    def test_userCreation(self):
        names = [user.first_name for user in UserData.objects.all()]
        self.assertEquals(self.testUsers, names)

    def test_userFriends(self):
        adam = UserData.objects.filter(first_name='Adam')[0]
        holly = UserData.objects.filter(first_name='Holly')[0]
        ben = UserData.objects.filter(first_name='Ben')[0]
        kelly = UserData.objects.filter(first_name='Kelly')[0]

        adam.friends.add(holly, ben)
        holly.friends.add(ben, kelly)

        ben.friends.add(kelly)

        adam_expected_friends = ['Holly', 'Ben']
        holly_expected_friends = ['Adam', 'Kelly', 'Ben']
        kelly_expected_friends = ['Holly', 'Ben']

        ben_expected_friends = ['Adam', 'Holly', 'Kelly']

        self.assertEquals(adam_expected_friends, [friend.first_name for friend in adam.friends.all()])
        self.assertEquals(holly_expected_friends, [friend.first_name for friend in holly.friends.all()])
        self.assertEquals(kelly_expected_friends, [friend.first_name for friend in kelly.friends.all()])
        self.assertEquals(ben_expected_friends, [friend.first_name for friend in ben.friends.all()])


class Test_Stations(BaseDelayRepayTesting):
    def test_all_stations(self):
        all_stations = Station.objects.all()
        stations_names = [station.name for station in all_stations]
        self.assertEquals(self.test_stations, stations_names)


class Test_Functional(LiveServerTestCase):
    testUsers = ['Adam', 'Holly', 'Kelly', 'Ben']
    test_stations = ['Earlswood (Surrey)', 'London Victoria']
    index = 'http://localhost:8081'

    def setUp(self):
        for name in self.testUsers:
            user = UserData()
            user.title = 'Mr'
            user.first_name = "%s" % name
            user.username = "User_%s" % name
            user.email = "%s@%s.com" % (user.first_name, user.first_name)
            user.set_password('testing')
            user.save()

            journey = Journey()
            journey.journeyName = utils.create_journey_name(self.test_stations[0], self.test_stations[1])
            journey.arrivingStation = self.test_stations[0]
            journey.departingStation = self.test_stations[1]
            journey.delayRepayUser = user
            journey.save()

            today = datetime.datetime.now().date()
            ticket = Ticket()
            ticket.cost = 330.00
            ticket.ticket_start_date = datetime.datetime(today.year, today.month -1, today.day)
            ticket.ticket_expiry_date = datetime.datetime(today.year, today.month + 1, today.day)
            ticket.delayRepayUser = user
            ticket.ticket_photo = SimpleUploadedFile('best_file_eva.txt', 'these are the file contents!')
            ticket.save()

            for count in xrange(0, 10):
                delay = Delay()
                date = datetime.datetime.now().date()
                if count % 2 == 0:
                    delay.date = date
                else:
                    delay.date = datetime.datetime(date.year+1, date.month+1, date.day+1).date()
                delay.startTime = datetime.datetime.now().time()
                delay.endTime = datetime.datetime.now().time()
                delay.delay = '30-59 mins'
                delay.delay_reason = 'Train cancelled'
                delay.delayRepayUser = user
                claimed = False
                if count % 2 != 0:
                    claimed = True
                delay.claimed = claimed
                delay.journey = journey
                delay.save()

        for station_name in self.test_stations:
            station = Station()
            station.name = station_name
            station.save()


        self.selenium = webdriver.PhantomJS()
        #self.selenium = webdriver.Chrome()
        self.selenium.maximize_window()
        super(Test_Functional, self).setUp()

    def tearDown(self):
        # Call tearDown to close the web browser
        time.sleep(TEARDOWN_TIME)
        self.selenium.quit()

        super(Test_Functional, self).tearDown()

    def login(self):
        self.selenium.get(self.index)
        wait()
        self.selenium.find_element_by_id('id_username').send_keys('User_Adam')
        wait()
        self.selenium.find_element_by_id('id_password').send_keys('testing')
        wait()
        self.selenium.find_element_by_id('submit-id-login').click()
        wait()

    def test_invalid_login(self):
        self.selenium.get(self.index)
        wait()
        self.selenium.find_element_by_id('submit-id-login').click()
        wait()
        expected_error = "Sorry, that's not a valid username or password"
        errors = self.selenium.find_elements_by_class_name("error")
        self.assertEquals(expected_error, errors[0].text)

    def test_valid_login(self):
        self.login()
        expected_title = "Welcome To Southern Fail Delay Repay"
        self.assertEquals(
            expected_title,
            self.selenium.find_element_by_id("page_title").text
        )

    def test_add_journey(self):
        self.login()
        self.selenium.get(self.index + '/addJourney')
        expected_title = "Add A Journey"
        wait()
        self.assertEquals(
            expected_title,
            self.selenium.find_element_by_id("page_title").text
        )

    def test_check_stations(self):
        self.login()
        self.selenium.get(self.index + '/addJourney')

        expected = "\n".join(self.test_stations)
        self.assertEquals(
            expected,
            self.selenium.find_element_by_id('id_departing_station').text
        )

    def add_friend(self, expected_email):
        expected_url = self.index + '/addFriend/'
        wait()
        self.selenium.find_element_by_id('id_addFriend').click()
        wait()
        self.assertEquals(expected_url, self.selenium.current_url)

        self.selenium.find_element_by_id('id_friend_email').send_keys(expected_email)
        wait()
        self.selenium.find_element_by_id('submit-id-add-friend').click()
        wait()

    def test_add_friend_valid(self):
        self.login()
        expected_email = 'Holly@Holly.com'
        self.add_friend(expected_email)

        adam = UserData.objects.filter(first_name='Adam')[0]

        friends = adam.friends.all()
        if not friends:
            self.assertEquals([], friends, 'No Friends Were Added')

        self.assertEquals(expected_email, friends[0].email)

    def test_add_friend_add_self(self):
        self.login()
        expected_email = 'Adam@Adam.com'
        self.add_friend(expected_email)

        adam = UserData.objects.filter(first_name='Adam')[0]

        friends = adam.friends.all()
        if friends:
            self.assertEquals([], friends, 'Friends Were Added')

        expected_error = "Cant add your own email address as a friend"
        errors = self.selenium.find_elements_by_class_name("alert-danger")
        self.assertEquals(expected_error, errors[0].text)

    def test_add_friend_invalid(self):
        self.login()
        expected_email = 'D@D.com'
        self.add_friend(expected_email)

        adam = UserData.objects.filter(first_name='Adam')[0]

        friends = adam.friends.all()
        if friends:
            self.assertEquals([], friends, 'Friends Were Added')

        expected_error = "No users matching email address provided found"
        errors = self.selenium.find_elements_by_class_name("alert-danger")
        self.assertEquals(expected_error, errors[0].text)

    def test_add_friend_twice(self):
        self.login()
        expected_email = 'Holly@Holly.com'
        self.add_friend(expected_email)
        self.add_friend(expected_email)

        expected_error = "This person is already your friend"
        errors = self.selenium.find_elements_by_class_name("alert-danger")
        self.assertEquals(expected_error, errors[0].text)

    def test_unclaimed_delays(self):
        self.login()
        expected_url = self.index + '/unclaimedDelays/'
        wait()
        self.selenium.find_element_by_id('id_unclaimedDelays').click()
        wait()
        self.assertEquals(expected_url, self.selenium.current_url)

    def test_submit_noJourneySelect(self):
        self.login()
        self.selenium.find_element_by_id('submit-id-submit-delay').click()
        expected_url = self.index + "/"
        self.assertEquals(expected_url, self.selenium.current_url)

    def test_submit_delay(self):
        self.login()
        wait()
        self.selenium.find_element_by_id('journeyItem1').click()
        wait()
        date = datetime.datetime.now()
        dateString = '%s/%s/%s' % (str(date.day-1), str(date.month), str(date.year))
        self.selenium.find_element_by_id('datepicker').send_keys(dateString)
        wait()
        self.selenium.find_element_by_id('timepicker2').send_keys('10:30')
        wait()
        self.selenium.find_element_by_id('timepicker').send_keys('9:30')
        wait(3)
        self.selenium.find_element_by_id('submit-id-submit-delay').click()
        expected_url = self.index + "/"
        wait(3)
        expected_title = "Welcome To Southern Fail Delay Repay"
        self.assertEquals(
            expected_title,
            self.selenium.find_element_by_id("page_title").text
        )




class TestUtils(BaseDelayRepayTesting):
    def test_create_journey_name(self):
        self.assertEquals(
            'A To B',
            utils.create_journey_name('A', 'B')
        )

    def test_get_todays_delays(self):
        adam = UserData.objects.filter(first_name='Adam')[0]
        delays = utils.get_delays_for_today(adam)
        self.assertEquals(5, len(delays))

    def get_browser_and_captcha(self):
        responseString, imagestring = utils.get_browser_and_captcha()

    def test_submit_delay(self):
        adam = UserData.objects.filter(first_name='Adam')[0]
        delays = Delay.objects.filter(delayRepayUser=adam)
        testdelay = None
        for delay in delays:
            if not delay.claimed:
                testdelay = delay
                break

        encodedResponse, encodedImage = utils.get_browser_and_captcha()
        result = utils.submit_delay(adam.username, testdelay, testdelay.journey, encodedResponse)
        self.assertEquals(result, True)

