from django.shortcuts import render
import evelink.api
import evelink.char
import evelink.eve
import evelink.account
from PyHq.libs.pyhqfunctions import *

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

        #get character sheet and format it for template
        char_sheet = char.character_sheet().result
        skill_tree = eve.skill_tree().result

        #get current skill in training
        current_training = char.current_training().result
        skillname = getSkillName(skill_tree, current_training['type_id'])

        #pump up the skill dict a bit to make viewing easier

        group_id_lookup = {}
        for group_id, group_values in skill_tree.iteritems():
            group_id_lookup[group_id] = group_values['name']

        for s in char_sheet['skills']:
            s['name'] = getSkillName(skill_tree, s['id'])











        return render(request, 'characteroverview.html', {'char_sheet' : char_sheet,
                                                          'faction_standings' : faction_standings,
                                                          'agent_standings' : agent_standings,
                                                          'corporation_standings' : corporation_standings,
                                                          'current_training' : current_training,
                                                          'skillname' : skillname,
                                                          'skilltree' : eve.skill_tree().result,
                                                          'skillgroups' : group_id_lookup})



def settings(request):
    changes = ""
    keyid = ""
    vcode = ""
    if request.POST:
        keyid = request.POST.get("keyid")
        vcode = request.POST.get("vcode")
        acct = Account.objects.filter(key_id=keyid)
        if acct:
            acct[0].v_code = vcode
            acct[0].key_id = keyid
            acct[0].save()
            changes = "Changes Saved!"
        else:
            acct = Account(key_id=request.POST.get("keyid"), v_code=request.POST.get("vcode"))
            acct.save()
            changes = "Account Created!"

    acct = Account.objects.all()
    if acct:
        keyid = acct[0].key_id
        vcode = acct[0].v_code
        request.session['keyid'] = keyid
        request.session['vcode'] = vcode
    return render(request, 'settings.html', {'changes' : changes, 'keyid' : keyid, 'vcode' : vcode})