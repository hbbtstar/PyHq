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

    def login(self, username, password):
        # login user
        c = Client()
        response = c.post('/login/', {'username': username, 'password': password})
        return response

    def setUp(self):
        print("Do nothing... yet")
        test_char = Character(name="Test Char", race="Test Race", bloodline="test_line", skill_points=1234567,
                              balance=12345678)
        test_user = User(username='test_user', password='testpass')
        test_account = Account()
        test_user.save()

    def login_screen_exists(self):
        # make sure login form exists
        c = Client()
        response = c.get("login/")
        self.assertIn(b'form method=', response.content)

    def invalid_user_cannot_log_in(self):
        c = Client()
        response = self.login('fleegfloog', 'fleegfleeg')
        self.assertIn(b'Please try again', response.content)

    def test_main_non_logged_in(self):
        #ensure that login screen happens for non_logged in user
        c = Client()
        response = c.get("/")
        self.assertIn(b"Please login", response.content)

    def test_main_logged_in(self):
        #ensure that user is redirected to settings
        c = Client()
        c.login('test_user', 'test_pass')
        response = c.get("/")
        self.assertIn(b'User Settings', response.content)


