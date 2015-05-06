from django.test import TestCase, Client
from PyHq.apps.characterscreen.models import *
from PyHq.libs.pyhqfunctions import *
import evelink

# Create your tests here.

class CharacterScreenTestCase(TestCase):

    def setUp(self):
        print("Do nothing... yet")
        test_char = Character(name="Test Char", race="Test Race", bloodline="test_line", skill_points=1234567,
                              balance=12345678)

    def test_skill_update(self):
        #test that the skills are imported and generated correctly
        EveSkillsToDB()
        test_skill = Skill.objects.get(skill_id=3424)
        self.assertIn(test_skill.name, "Energy Grid Upgrades")

    #def test_skills_appear_to_logged_in_user(self):
        # test that skills appear in the template to a logged in user

    #def test_char_stats_appear_to_logged_in_user(self):
        # test that the character's stats appear to the logged in user
        #C = Client()
        #C.session.






