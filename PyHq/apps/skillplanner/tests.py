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
        response = c.get('/skillplanner/', {'skill': 'Energy Grid Upgrades'})
        self.assertIn(b'Energy Grid Upgrades', response.content)

    def test_invalid_skill_error(self):
        #make sure invalid skill returns error
        c = Client()
        c.login(username='test_user', password='test_pass')
        response = c.get('/skillplanner/', {'skill': 'Foo Laser Destructor'})
        self.assertIn(b'skill not found', response.content)

    def test_add_to_queue(self):
        #add to queue button pressed, should add a skill to the training queue only once
        c = Client()
        c.login(username='test_user', password='test_pass')
        response = c.get('/skillplanner/', {'skill': 'Weapon Upgrades', 'level': '5'})
        self.assertIn(b'<td>Weapon Upgrades</td>', response.content)
        self.assertEqual(response.content.count(b'<td>Weapon Upgrades</td>'), 1)

    def test_training_queue_loads(self):
        #check that an existing training queue loads initially
        c = Client()
        c.login(username='test_user', password='test_pass')
        new_skill = TrainingQueueRow.objects.create(char=Character.objects.all()[0],
                                                    skill=Skill.objects.get(name='Weapon Upgrades'), to_level = 5,
                                                    from_level = 4, position=1)
        new_skill.save()
        response = c.get('/skillplanner/')
        self.assertIn(b'<td>Weapon Upgrades</td>', response.content)

    def test_skillplanner_get_skill(self):
        #test get API
        c = Client()
        c.login(username='test_user', password='test_pass')
        response = c.get('/skillplanner/3424')
        self.assertIn(b'Energy Grid Upgrades', response.content)

    def test_disable_invalid_levels(self):
        # make sure user cannot select invalid to levels
        c = Client()
        c.login(username='test_user', password='test_pass')
        response = c.get('/skillplanner')
        self.assertIn(b'disabled>4', response.content)






