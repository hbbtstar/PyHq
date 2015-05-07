from __future__ import division
from django.shortcuts import render
import evelink.api
import evelink.char
import evelink.eve
import evelink.account
from PyHq.libs.pyhqfunctions import *
from datetime import datetime, timedelta
import time
from PyHq.settings import LEVEL_BASE
from django.contrib.auth.decorators import login_required

from PyHq.apps.characterscreen.models import *



# this will have to be rolled into initial setup at some point
def debug(request):
    EveSkillsToDB()
    eve = evelink.eve.EVE()
    api = evelink.api.API(api_key=(request.session['keyid'], request.session['vcode']))
    newacct = evelink.account.Account(api)
    tempcharlist = newacct.characters()[0]
    char_id = list(tempcharlist)[0]
    char = evelink.char.Char(char_id=char_id, api=api)
    tempaccount = Account.objects.get(v_code=request.session['vcode'])
    CreateChar(char_id, api, tempaccount)
    skills = Skill.objects.all()
    return render(request, 'debugpage.html', {'skills' : skills})

@login_required
def character(request):
    acct = Account.objects.get(user=User.objects.get(username=request.user.get_username()))
    keyid = acct.key_id
    vcode = acct.v_code
    if keyid:
        # get some character stuff
        eve = evelink.eve.EVE()
        api = evelink.api.API(api_key=(keyid, vcode))
        request.session['char_id'] = Character.objects.get(acct.characters.all()[0].char_id)
        char_object = Character.objects.get(acct.characters.all()[0])
        # char = evelink.char.Char(char_id=char_id, api=api)
        UpdateChar(char_object.char_id, api)
        faction_standings = []
        corporation_standings = []
        agent_standings = []
        char_standings = char_object.standings
        char_sheet = char_object
        # get effective standings by applying the effective standings equation to our standings
        conn_dip_skills = {}
        conn_dip_skills['diplo'] = 0
        conn_dip_skills['conn'] = 0

        for i in char_sheet.skills:
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
                    s['standing'] + ((10-s['standing'])*(0.04*(conn_dip_skills['diplo']))), 2)
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
        for s in char_sheet.skills:
            temp_skill = Skill.objects.get(skill_id=s['id'])
            s['name'] = temp_skill.name
            s['group_id'] = temp_skill.group_id
            s['rank'] = temp_skill.rank
        group_tree.order_by('name')

        #get current skill in training
        current_training = char_object.current_training
        skillname = ''
        if current_training['level'] is None:
            current_training['name'] = 'None'
        else:
            current_training['name'] = Skill.objects.get(skill_id=current_training['type_id']).name


        #get skill queue names too and format the numbers nicely
        skill_queue = char_object.skill_queue

        #skip this if skill queue is paused
        if skill_queue[0]['end_ts'] is not None:
            for x in skill_queue:
                cur_skill = Skill.objects.get(skill_id=x['type_id'])
                x['name'] = cur_skill.name
                x['rank'] = cur_skill.rank
                for i in char_sheet.skills:
                    if cur_skill.skill_id == i['id']:
                        x['sp'] = i['skillpoints']
                sec = timedelta(seconds=(x['end_ts'] - time.time()))
                d = datetime(1,1,1) + sec
                x['end_date'] = "{0}d {1}h {2}m {3}s".format(d.day - 1, d.hour, d.minute, d.second)
            # get us some percentages
                modifier = LEVEL_BASE['L1']
                if x['level'] == 2:
                    modifier = LEVEL_BASE['L2']
                elif x['level'] == 3:
                    modifier = LEVEL_BASE['L3']
                elif x['level'] == 4:
                    modifier = LEVEL_BASE['L4']
                elif x['level'] == 5:
                    modifier = LEVEL_BASE['L5']
                time_span = x['end_ts'] - x['start_ts']
                s_time_span = time.time() - x['start_ts']
                cur_sp = s_time_span / time_span * (x['end_sp'] - x['start_sp'])
                x['percent_done'] = round(100 * (s_time_span / time_span))


            # x['percent_done'] = round(100*(x['start_ts'] / x['end_ts']))

        #get certificates


        return render(request, 'characteroverview.html', {'char_sheet' : char_sheet,
                                                          'faction_standings': faction_standings,
                                                          'agent_standings': agent_standings,
                                                          'corporation_standings': corporation_standings,
                                                          'current_training': current_training,
                                                          'group_tree': group_tree,
                                                          'skill_queue': skill_queue})





