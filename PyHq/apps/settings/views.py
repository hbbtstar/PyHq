from django.shortcuts import render
import evelink.api
import evelink.char
import evelink.eve
import evelink.account
from PyHq.apps.characterscreen.models import Account
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required
def settings(request):
    changes = ""
    keyid = ""
    vcode = ""
    current_user = User.objects.get(username=request.user.get_username())
    print(Account.objects.filter(user=current_user).exists())
    if not request.POST and not Account.objects.filter(user=current_user).exists():
        first_time = "We can see it's your first time using the program! Enter your keyid and vcode to get started."
        return render(request, 'settings.html', {'first_time': first_time})
    if request.POST:
        # how did we even get here?
        if not request.POST.get("keyid") or not request.POST.get("vcode"):
            return render(request, 'settings.html')
        elif Account.objects.filter(user=request.user).exists():
            acct = Account.objects.get(user=request.user)
            acct.key_id = request.POST.get("keyid")
            acct.v_code = request.POST.get("vcode")
            acct.save()
            return render(request, 'settings.html', {'changes': 'Account Saved!'})
        else:
            acct = Account(key_id=request.POST.get("keyid"), v_code=request.POST.get("vcode"), user=request.user)
            acct.save()
            return render(request, 'settings.html', {'changes': 'Account Created!'})
    elif request.user.is_authenticated():
        acct = Account.objects.get(user=current_user)
        vcode = acct.v_code
        keyid = acct.key_id
        return render(request, "settings.html", {'keyid': keyid, 'vcode': vcode })




