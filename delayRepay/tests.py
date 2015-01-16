import time
from selenium import webdriver

from django.test import TestCase, LiveServerTestCase
from delayRepay.models import UserData


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


class Test_Functional(LiveServerTestCase):
    def setUp(self):
        self.selenium = webdriver.Chrome()
        self.selenium.maximize_window()
        super(Test_Functional, self).setUp()

    def tearDown(self):
        # Call tearDown to close the web browser
        time.sleep(2)
        self.selenium.quit()

        super(Test_Functional, self).tearDown()

    def test_register(self):
        self.selenium.get('http://localhost:8081')
        self.selenium.find_element_by_id('submit-id-login').click()

        self.assertEquals(1 + 2, 1)


