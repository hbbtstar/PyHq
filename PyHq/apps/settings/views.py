from django.shortcuts import render
import evelink.api
import evelink.char
import evelink.eve
import evelink.account
from PyHq.apps.characterscreen.models import Account
from django.contrib.auth.models import User

def settings(request):
    changes = ""
    keyid = ""
    vcode = ""
    if request.POST:
        if not request.POST.get("keyid") or not request.POST.get("vcode"):
            return render(request, 'settings.html')
        else:
            keyid = request.POST.get("keyid")
            vcode = request.POST.get("vcode")
            print(request.user)
            user = User.objects.get(username=request.user.username)

            acct = Account.objects.filter(key_id=keyid)
            if acct:
                acct[0].v_code = vcode
                acct[0].key_id = keyid
                acct[0].save()
                changes = "Changes Saved!"
            else:
                acct = Account(key_id=request.POST.get("keyid"), v_code=request.POST.get("vcode"), user=user)
                acct.save()
                changes = "Account Created!"

    acct = Account.objects.all()
    if acct:
        keyid = acct[0].key_id
        vcode = acct[0].v_code
        request.session['keyid'] = keyid
        request.session['vcode'] = vcode
    else:
        first_time = "We can see it's your first time using the program."
    return render(request, 'settings.html', {'changes' : changes, 'keyid' : keyid, 'vcode' : vcode})
