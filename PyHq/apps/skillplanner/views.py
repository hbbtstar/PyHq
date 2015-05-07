from django.shortcuts import render, render_to_response, redirect
from PyHq.apps.characterscreen.models import *
import json
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
import evelink

# Create your views here.
def get_skills(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        skills = Skill.objects.filter(name__icontains=q)
        results = []
        for skill in skills:
            skill_json = {}
            skill_json['id'] = skill.skill_id
            skill_json['label'] = skill.name
            skill_json['value'] = skill.name
            results.append(skill_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype='application/json'
    return HttpResponse(data, mimetype)

# def load_skills(request):
#     if request.is_ajax():
#         q = request.GET.get('skill', '')
#         skill = Skill.objects.get(name__iexact=q)
#         results = []
#         skill_json = {}
#         skill_json['skill_id'] = skill.skill_id
#         skill_json['name'] = skill.name
#         skill_json['rank'] = skill.rank
#         skill_json['primaryAttribute'] = skill.primaryAttribute.title()
#         skill_json['secondaryAttribute'] = skill.secondaryAttribute.title()
#         skill_json['description'] = skill.description
#         skill_json['prereqs'] = {}
#
#         # get minimum level the skill can be trained to
#         char = Character.objects.get(id=request.session['char_id'])
#         cur_level = 0
#         for i in char.skills:
#             if i['id'] == skill.skill_id:
#                 cur_level = i['level']
#         skill_json['min_level'] = cur_level
#         prereq_set = RequiredSkill.objects.filter(from_skill_id=skill.skill_id)
#         for i in prereq_set:
#             prereq_skill = Skill.objects.get(skill_id=i.required_id)
#             prereq_name = prereq_skill.name
#             skill_json['prereqs'][prereq_name] = i.required_level
#         results.append(skill_json)
#         data = json.dumps(results)
#     else:
#         data = 'fail'
#     mimetype='application/json'
#     return HttpResponse(data, mimetype)
#
# def add_to_queue(request):
#     if request.is_ajax():
#         q = request.GET['skill']
#         get_to_level = int(request.GET['level'])
#         skill = Skill.objects.get(name__iexact=q)
#         char = Character.objects.get(id=request.session['char_id'])
#         results = []
#         skill_json = []
#         time_to_complete = 0
#         skill_json.append(skill.name)
#         for i in char.skills:
#             if i['id'] == skill.skill_id:
#
#
#                 # get skill current level
#                 cur_level = i['level']
#                 from_level = cur_level
#
#
#                 to_level = from_level + 1
#                 percentage = '100%'
#                 training_time = 'training time'
#                 time_to_complete = 0
#                 date_completed = '08:52 PM 04/15/2012'
#                 skill_json.extend([cur_level, from_level, to_level, percentage, training_time, time_to_complete, date_completed])
#         mimetype = 'application/json'
#         results.append(skill_json)
#         data = json.dumps(results)
#         return HttpResponse(data, mimetype)




@login_required
def get_skill(request, skill_id=None):
    if not skill_id:
        return redirect('/skillplanner/')
    else:
        ret_skill = Skill.objects.get(skill_id=skill_id)
        return HttpResponse(json.dumps(ret_skill), content_type="application/json")



@login_required
def skillplanner(request):
    acct = Account.objects.get(user=User.objects.get(username=request.user.get_username()))
    character = Character.objects.get(account_id=acct)
    api = evelink.api.API(api_key=(acct.key_id, acct.v_code))
    char = evelink.char.Char(char_id=character.id, api=api)
    char_sheet = char.character_sheet().result
    if request.GET.get('level'):
        skill_to_add = Skill.objects.get(name=request.GET.get('skill'))
        # means they want to add the skill to the queue
        try:
            skill_to_add = Skill.objects.get(name=request.GET.get('skill'))
        except ObjectDoesNotExist:
            return render_to_response('snippets/skillplanner/training_queue.html')

        to_level = int(request.GET.get('level'))
        from_level = 1
        # check if character level is higher than to_level. If so, raise to_level to character level + 1
        for skill in char_sheet['skills']:
            if skill_to_add.skill_id == skill['id']:
                from_level = skill['level']

        if from_level >= to_level:
            to_level = from_level + 1

        # check if queue exists. If so, check if skill is already there and change to and from levels accordingly.
        # also make sure that to_level is not already 5
        training_queue = TrainingQueueRow.objects.filter(char=character).order_by('position')
        position = 1
        if training_queue.exists():
            training_queue.reverse()
            for t_skill in training_queue:
                if t_skill.skill.skill_id == skill_to_add.skill_id:
                    if t_skill.to_level == 5:
                        return HttpResponse('error! Cannot train skill past 5.')
                    if t_skill.to_level > to_level:
                        to_level = t_skill.to_level
                    if t_skill.from_level > from_level:
                        from_level = t_skill.from_level
                        break
            position = training_queue[0].position + 1

        # some sanity checking to make sure that to_level and from_level are not over 6
        if to_level > 5 or from_level > 4:
            return HttpResponse('error! Cannot train skill past 5.')

        new_skill = TrainingQueueRow.objects.create(char=character, skill=skill_to_add, from_level=from_level,
                                            to_level=to_level, position=position)
        queue = list(training_queue.reverse())
        new_skill.save()
        return render_to_response('snippets/skillplanner/training_queue.html', {'queue': queue})










    elif request.GET.get('skill') and not request.GET.get('level'):
        #make sure the skill is valid
        try:
            skill = Skill.objects.get(name=request.GET.get('skill'))
        except ObjectDoesNotExist:
            return HttpResponse("skill not found!")
        return render_to_response('snippets/skillplanner/skillpane.html', {'skill': skill})

    else:
        try:
            queue = list(TrainingQueueRow.objects.order_by('position'))
        except:
            return render(request,'skillplanner.html')

    queue = TrainingQueueRow.objects.filter(char=character).order_by('position')

    return render(request, 'skillplanner.html', {'queue': queue})

















    acct = Account.objects.get(user=User.objects.get(username=request.user.get_username()))
    keyid = acct.key_id
    vcode = acct.v_code
    # get some character stuff
    eve = evelink.eve.EVE()
    api = evelink.api.API(api_key=(keyid, vcode))
    char_object = Character.objects.get(account_id=acct)
    return render(request, 'skillplanner.html')



