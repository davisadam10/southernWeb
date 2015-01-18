import time
from selenium import webdriver

from django.test import TestCase, LiveServerTestCase
from delayRepay.models import UserData, Station

TEARDOWN_TIME = 0


# Create your tests here.
class UserModelTests(TestCase):
    testUsers = ['Adam', 'Holly', 'Kelly', 'Ben']

    def setUp(self):
        for name in self.testUsers:
            user = UserData()
            user.first_name = "%s" % name
            user.username = "User_%s" % name
            user.save()

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


class Test_Stations(TestCase):
    test_stations = ['Earlswood (Surrey)', 'London Victoria']

    def setUp(self):
        for station_name in self.test_stations:
            station = Station()
            station.name = station_name
            station.save()

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
            user.first_name = "%s" % name
            user.username = "User_%s" % name
            user.set_password('testing')
            user.save()

        for station_name in self.test_stations:
            station = Station()
            station.name = station_name
            station.save()

        self.selenium = webdriver.Chrome()
        self.selenium.maximize_window()
        super(Test_Functional, self).setUp()

    def tearDown(self):
        # Call tearDown to close the web browser
        time.sleep(TEARDOWN_TIME)
        self.selenium.quit()

        super(Test_Functional, self).tearDown()

    def login(self):
        self.selenium.get(self.index)
        self.selenium.find_element_by_id('id_username').send_keys('User_Adam')
        self.selenium.find_element_by_id('id_password').send_keys('testing')
        self.selenium.find_element_by_id('submit-id-login').click()

    def test_invalid_login(self):
        self.selenium.get(self.index)
        self.selenium.find_element_by_id('submit-id-login').click()

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

