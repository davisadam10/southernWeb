from django.test import TestCase
from delayRepay.models import UserData, Journey


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

