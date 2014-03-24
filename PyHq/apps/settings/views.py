from django.shortcuts import render
import evelink.api
import evelink.char
import evelink.eve
import evelink.account
from PyHq.apps.characterscreen.models import Account

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
