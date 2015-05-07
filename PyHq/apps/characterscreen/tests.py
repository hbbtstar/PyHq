from django.test import TestCase, Client
from PyHq.apps.characterscreen.models import *
from PyHq.libs.pyhqfunctions import *
import evelink

# Create your tests here.

class CharacterScreenTestCase(TestCase):

    def user_login(self, username, password):
        # login user
        c = Client()
        response = c.post('/login/', {'username': username, 'password': password})
        return response

    def setUp(self):
        print("Do nothing... yet")
        test_user = User.objects.create_user(username='test_user', email='f@f.com', password='test_pass')
        test_user.save()
        test_account = Account(v_code='12345', key_id='12345', user=test_user)
        test_account.save()
        test_char = Character(id=99999, name="Test Char", race="Test Race", bloodline="test_line", skill_points=1234567,
                              balance=12345678, account_id=test_account)
        test_char.save()
        fake_skill = Skill(skill_id=99999, name='Fake Skill', group_id=2, description='test description', rank=3,
                           primaryAttribute='Intelligence', secondaryAttribute='Charisma')
        fake_skill.save()

    def test_skill_update(self):
        #test that the skills are imported and generated correctly
        EveSkillsToDB()
        test_skill = Skill.objects.get(skill_id=3424)
        self.assertIn(test_skill.name, "Energy Grid Upgrades")

    #def test_char_stats_appear_to_logged_in_user(self):
        # test that the character's stats appear to the logged in user
        #C = Client()
        #C.session.






