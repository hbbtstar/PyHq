from django.test import TestCase, Client
from PyHq.apps.characterscreen.models import *
from PyHq.libs.pyhqfunctions import *
import evelink
from PyHq.secret_settings import V_CODE, KEY_ID


class SkillPlannerTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        EveSkillsToDB()
        test_user = User.objects.create_user(username='test_user', email='f@f.com', password='test_pass')
        test_user.save()
        test_account = Account(v_code=V_CODE, key_id=KEY_ID, user=test_user)
        test_account.save()
        api = evelink.api.API(api_key=(KEY_ID, V_CODE))
        newacct = evelink.account.Account(api)
        tempcharlist = newacct.characters()[0]
        char_id = list(tempcharlist)[0]
        char = evelink.char.Char(char_id=char_id, api=api)
        CreateChar(char_id, api, test_account)

    def setUp(self):
        # test_char = Character(id=99999, name="Test Char", race="Test Race", bloodline="test_line", skill_points=1234567,
        #                       balance=12345678, account_id=test_account)
        # test_char.save()
        fake_skill = Skill(skill_id=99999, name='Fake Skill', group_id=2, description='test description', rank=3,
                           primaryAttribute='Intelligence', secondaryAttribute='Charisma')
        fake_skill.save()

    def test_invalid_user_cannot_access(self):
        #make sure unauthorized users can't log in
        c = Client()
        c.logout()
        response = c.get("/skillplanner/", follow=True)
        self.assertIn(b'please login', response.content)

    def test_valid_user_can_access(self):
        #make sure valid user sees the page
        c = Client()
        c.login(username='test_user', password='test_pass')
        response = c.get("/skillplanner/", follow=True)
        self.assertIn(b'Skill Name', response.content)

    def test_skill_pane_loads(self):
        #make sure skill div loads
        c = Client()
        c.login(username='test_user', password='test_pass')
        response = c.post('/skillplanner/', {'skill': 'Energy Grid Upgrades'})
        self.assertIn(b'Energy Grid Upgrades', response.content)

