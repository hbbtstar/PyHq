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
        # test_char = Character(name="Test Char", race="Test Race", bloodline="test_line", skill_points=1234567,
        #                       balance=12345678)
        # test_user = User(username='test_user', password='test_pass')
        # test_user.save()
        # test_char.save()
        # test_account = Account(vcode='12345', keyid='12345', user=test_user)
        # test_account.save()
        # fake_skill = Skill(name='Fake Skill', group_id=2, description='test description', rank=3,
        #                    primaryAttribute='Intelligence', secondaryAttribute='Charisma')
        # fake_skill.save()
        # fake_points = CharacterSkillPoints(skill=fake_skill, char=test_char, points=12345, level=3)
        # fake_points.save()

    def test_skill_update(self):
        #test that the skills are imported and generated correctly
        EveSkillsToDB()
        test_skill = Skill.objects.get(skill_id=3424)
        self.assertIn(test_skill.name, "Energy Grid Upgrades")

    def test_skills_appear(self):
        #test that skills appear in dropdown
        self.user_login(username='test_char', password='test_pass')
        c = Client()
        response = c.get('/characterscreen/')
        self.AssertIn(b'Fake Skill', response.content)


    #def test_char_stats_appear_to_logged_in_user(self):
        # test that the character's stats appear to the logged in user
        #C = Client()
        #C.session.






