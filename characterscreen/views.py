from django.shortcuts import render
from characterscreen.models import *
import evelink.api
import evelink.char
import evelink.eve
import evelink.account

from django.http import HttpResponse

def index(request):
    return render(request, 'generic_base.html')

def character(request):
    # get some character stuff
    eve = evelink.eve.EVE()
    api = evelink.api.API(api_key=(request.session['keyid'], request.session['vcode']))
    # this is really kludgy, but I have no idea how else to to do it. Doing an account API call
    # and unpacking the dict for the character ID
    newacct = evelink.account.Account(api)
    tempcharlist = newacct.characters()[0]
    char_id = list(tempcharlist)[0]
    char = evelink.char.Char(char_id = char_id, api=api)
    faction_standings = []
    corporation_standings = []
    agent_standings = []

    for x in char.standings().result['factions'].items():
        faction_standings.append(x[1])
    for x in char.standings().result['corps'].items():
        corporation_standings.append(x[1])
    for x in char.standings().result['agents'].items():
        agent_standings.append(x[1])

    faction_standings = sorted(faction_standings, key=lambda k: k['name'])
    corporation_standings = sorted(corporation_standings, key=lambda k: k['name'])
    agent_standings = sorted(agent_standings, key=lambda k: k['name'])

    return render(request, 'characteroverview.html', {'char' : char, 'faction_standings' : faction_standings,
                  'agent_standings' : agent_standings, 'corporation_standings' : corporation_standings})



def settings(request):
    changes = ""
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


    else:
        acct = Account.objects.all()
        if acct:
            keyid = acct[0].key_id
            vcode = acct[0].v_code
            request.session['keyid'] = keyid
            request.session['vcode'] = vcode
            return render(request, 'settings.html', {'changes' : changes, 'keyid' : keyid, 'vcode' : vcode})
    return render(request, 'settings.html')