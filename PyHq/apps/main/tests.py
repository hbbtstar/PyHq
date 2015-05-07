from django.test import TestCase

# Create your tests here.


from django.test import TestCase, Client
from PyHq.apps.characterscreen.models import *
from django.contrib.auth.models import User
from PyHq.libs.pyhqfunctions import *
import evelink

# Create your tests here.

class MainTestCase(TestCase):

    #helper functions

    def user_login(self, username, password):
        # login user
        c = Client()
        response = c.post('/accounts/login/', {'username': username, 'password': password}, follow=True)
        return response

    def setUp(self):
        print("Do nothing... yet")
        self.test_user = User.objects.create_user(username='test_user', email="email@email.com", password='test_pass')
        self.test_user.save()
        # test_char = Character(name="Test Char", race="Test Race", bloodline="test_line", skill_points=1234567,
        #                       balance=12345678)
        #
        # test_char.save()
        # fake_skill = Skill(name='fake_skill', group_id=2, description='test description', rank=3,
        #                    primaryAttribute='Intelligence', secondaryAttribute='Charisma')
        # fake_skill.save()
        # fake_points = CharacterSkillPoints(skill=fake_skill, char=test_char, points=12345, level=3)
        # fake_points.save()

    def tearDown(self):
        self.test_user.delete()

    def login_screen_exists(self):
        # make sure login form exists
        c = Client()
        response = c.get("login/")
        self.assertIn(b'form method=', response.content)

    def invalid_user_cannot_log_in(self):
        c = Client()
        response = self.user_login(username='fleegfloog', password='fleegfleeg')
        self.assertIn(b'Please try again', response.content)

    def test_main_non_logged_in(self):
        #ensure that login screen happens for non_logged in user
        c = Client()
        c.logout()
        response = c.get("/", follow=True)
        self.assertIn(b"please login", response.content)

    def test_main_logged_in(self):
        #ensure that user can log in and is redirected to settings
        c = Client()
        response = self.user_login(username='test_user', password='test_pass')
        self.assertIn(b'User Settings', response.content)

    def test_first_time(self):
        #check that system detects first time user
        c = Client()
        c.logout()
        c.login(username='test_user', password='test_pass')
        response = c.get("/settings", follow=True)
        self.assertIn(b'first time', response.content)

    def test_account_creation(self):
        #check that account creation goes off successfully
        c = Client()
        c.logout()
        Account.objects.all().delete()
        c.login(username='test_user', password='test_pass')
        response = c.post('/settings/', {'vcode': '345Xgfh43', 'keyid': '122345'})
        self.assertIn(b'Account Created', response.content)

    def test_account_update(self):
        #if account exists, update it
                #check that account creation goes off successfully
        c = Client()
        c.logout()
        acct = Account(key_id='132345', v_code='xcdF56Gh', user=User.objects.get(username='test_user'))
        acct.save()
        c.login(username='test_user', password='test_pass')
        response = c.post('/settings/', {'vcode': '345Xgfh43', 'keyid': '122345'})
        self.assertIn(b'Account Saved', response.content)
