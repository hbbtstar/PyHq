from django.shortcuts import render
import evelink.api
import evelink.char
import evelink.eve
import evelink.account
from PyHq.libs.pyhqfunctions import *
from datetime import datetime, timedelta
import time

from PyHq.apps.characterscreen.models import *


def debug(request):
    EveSkillsToDB()
    skills = Skill.objects.all()
    return render(request, 'debugpage.html', {'skills' : skills})

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
        char_standings = char.standings().result
        char_sheet = char.character_sheet().result
        # get effective standings by applying the effective standings equation to our standings
        conn_dip_skills = {}
        conn_dip_skills['diplo'] = 0
        conn_dip_skills['conn'] = 0

        for i in char_sheet['skills']:
            if i['id'] == 3357:
                conn_dip_skills['diplo'] = i['level']

            if i['id'] == 3359:
                conn_dip_skills['conn'] = i['level']

        for v, s in char_standings['factions'].items():
            if s['standing'] < 0:
                char_standings['factions'][s['id']]['e_standing'] = round(
                    (s['standing'] +((10-s['standing'])*(0.04*(conn_dip_skills['diplo'])))), 2)
            else:
                char_standings['factions'][s['id']]['e_standing'] = round(
                    s['standing'] + ((10-s['standing'])*(0.04*(conn_dip_skills['conn']))), 2)
        for v,s in char_standings['agents'].items():
            if s['standing'] < 0:
                char_standings['agents'][s['id']]['e_standing'] = round(
                    s['standing'] + ((10-s['standing'])*(0.04*(conn_dip_skills['diplo']))), 2)
            else:
                char_standings['agents'][s['id']]['e_standing'] = round(
                    s['standing'] + ((10-s['standing'])*(0.04*(conn_dip_skills['conn']))), 2)
        for v,s in char_standings['corps'].items():
            if s['standing'] < 0:
                char_standings['corps'][s['id']]['e_standing'] = round(
                    s['standing'] + ((10-s['standing'])*(0.04*(conn_dip_skills['diplo']))),2)
            else:
                char_standings['corps'][s['id']]['e_standing'] = round(
                    s['standing'] + ((10-s['standing'])*(0.04*(conn_dip_skills['conn']))), 2)




        # get the standings and order them into a list
        for x in char_standings['factions'].items():
            faction_standings.append(x[1])
        for x in char_standings['corps'].items():
            corporation_standings.append(x[1])
        for x in char_standings['agents'].items():
            agent_standings.append(x[1])

        faction_standings = sorted(faction_standings, key=lambda k: k['name'])
        corporation_standings = sorted(corporation_standings, key=lambda k: k['name'])
        agent_standings = sorted(agent_standings, key=lambda k: k['name'])

        #get character sheet and format it for template, make the skills all nice and alphabetical

        group_tree = SkillGroup.objects.all().exclude(skill_group_id=505)
        for s in char_sheet['skills']:
            temp_skill = Skill.objects.get(skill_id=s['id'])
            s['name'] = temp_skill.name
            s['group_id'] = temp_skill.group_id
            s['rank'] = temp_skill.rank
        group_tree.order_by('name')



        #pop out the fake skills group so it doesn't show in the final page
        # for x in skill_tree:
        #     if x['skill_group_id'] == 505:
        #         skill_tree.remove(x)


        # skill_tree = sorted(skill_tree, key=lambda k: k['name'])

        #get current skill in training
        current_training = char.current_training().result
        skillname = ''
        current_training['name'] = Skill.objects.get(skill_id=current_training['type_id']).name



        #get skill queue names too and format the numbers nicely
        skill_queue = char.skill_queue().result
        for x in skill_queue:
            x['name'] = Skill.objects.filter(skill_id=x['type_id'])[0].name
            sec = timedelta(seconds=(x['end_ts'] - time.time()))
            d = datetime(1,1,1) + sec
            x['end_date'] = "{0}d {1}h {2}m {3}s".format(d.day - 1, d.hour, d.minute, d.second)
        # get us some percentages
            x['percent_done'] = round(100 * x['start_sp'] / x['end_sp'])
        #get certificates


        return render(request, 'characteroverview.html', {'char_sheet' : char_sheet,
                                                          'faction_standings': faction_standings,
                                                          'agent_standings': agent_standings,
                                                          'corporation_standings': corporation_standings,
                                                          'current_training': current_training,
                                                          'group_tree': group_tree,
                                                          'skill_queue': skill_queue})




