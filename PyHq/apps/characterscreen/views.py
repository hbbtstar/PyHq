from django.shortcuts import render
import evelink.api
import evelink.char
import evelink.eve
import evelink.account
from PyHq.libs.pyhqfunctions import *
from datetime import datetime, timedelta
import time

from PyHq.apps.characterscreen.models import *


def index(request):
    return render(request, 'generic_base.html')

def character(request):
    keyid = request.session.get('keyid')
    if keyid:
        # get some character stuff
        eve = evelink.eve.EVE()
        api = evelink.api.API(api_key=(request.session['keyid'], request.session['vcode']))
        # this is really kludgy, but I have no idea how else to to do it. Doing an account API call
        # and unpacking the dict for the character ID
        newacct = evelink.account.Account(api)
        tempcharlist = newacct.characters()[0]
        char_id = list(tempcharlist)[0]
        char = evelink.char.Char(char_id=char_id, api=api)
        faction_standings = []
        corporation_standings = []
        agent_standings = []

        # get the standings and order them into a list
        for x in char.standings().result['factions'].items():
            faction_standings.append(x[1])
        for x in char.standings().result['corps'].items():
            corporation_standings.append(x[1])
        for x in char.standings().result['agents'].items():
            agent_standings.append(x[1])

        faction_standings = sorted(faction_standings, key=lambda k: k['name'])
        corporation_standings = sorted(corporation_standings, key=lambda k: k['name'])
        agent_standings = sorted(agent_standings, key=lambda k: k['name'])

        #get character sheet and format it for template, make the skills all nice and alphabetical
        char_sheet = char.character_sheet().result
        skill_tree = []
        for x in eve.skill_tree().result.items():
            skill_tree.append(x[1])

        #pop out the fake skills group so it doesn't show in the final page
        for x in list(skill_tree):
            if x['id'] == 505:
                skill_tree.remove(x)


        skill_tree = sorted(skill_tree, key=lambda k: k['name'])

        #get current skill in training
        current_training = char.current_training().result
        skillname = getSkillName(eve.skill_tree().result, current_training['type_id'])

        #get skill queue names too and format the numbers nicely
        skill_queue = char.skill_queue().result
        for x in skill_queue:
            x['name'] = getSkillName(eve.skill_tree().result, x['type_id'])
            sec = timedelta(seconds=(x['end_ts'] - time.time()))
            d = datetime(1,1,1) + sec
            x['end_date'] = "{0}d {1}h {2}m {3}s".format(d.day - 1, d.hour, d.minute, d.second)
        # get us some percentages
            x['percent_done'] = round(100 * x['start_sp'] / x['end_sp'])
        #get certificates


        return render(request, 'characteroverview.html', {'char_sheet' : char_sheet,
                                                          'faction_standings' : faction_standings,
                                                          'agent_standings' : agent_standings,
                                                          'corporation_standings' : corporation_standings,
                                                          'current_training' : current_training,
                                                          'skillname' : skillname,
                                                          'skilltree' : skill_tree,
                                                          'skill_queue' : skill_queue})




