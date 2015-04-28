from django.shortcuts import render
from PyHq.apps.characterscreen.models import *
import json
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
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

def load_skills(request):
    if request.is_ajax():
        q = request.GET.get('skill', '')
        skill = Skill.objects.get(name__iexact=q)
        results = []
        skill_json = {}
        skill_json['skill_id'] = skill.skill_id
        skill_json['name'] = skill.name
        skill_json['rank'] = skill.rank
        skill_json['primaryAttribute'] = skill.primaryAttribute.title()
        skill_json['secondaryAttribute'] = skill.secondaryAttribute.title()
        skill_json['description'] = skill.description
        skill_json['prereqs'] = {}

        # get minimum level the skill can be trained to
        char = Character.objects.get(id=request.session['char_id'])
        cur_level = 0
        for i in char.skills:
            if i['id'] == skill.skill_id:
                cur_level = i['level']
        skill_json['min_level'] = cur_level
        prereq_set = RequiredSkill.objects.filter(from_skill_id=skill.skill_id)
        for i in prereq_set:
            prereq_skill = Skill.objects.get(skill_id=i.required_id)
            prereq_name = prereq_skill.name
            skill_json['prereqs'][prereq_name] = i.required_level
        results.append(skill_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype='application/json'
    return HttpResponse(data, mimetype)

def add_to_queue(request):
    if request.is_ajax():
        q = request.GET['skill']
        get_to_level = int(request.GET['level'])
        skill = Skill.objects.get(name__iexact=q)
        char = Character.objects.get(id=request.session['char_id'])
        results = []
        skill_json = []
        time_to_complete = 0
        skill_json.append(skill.name)
        for i in char.skills:
            if i['id'] == skill.skill_id:


                # get skill current level
                cur_level = i['level']
                from_level = cur_level


                to_level = from_level + 1
                percentage = '100%'
                training_time = 'training time'
                time_to_complete = 0
                date_completed = '08:52 PM 04/15/2012'
                skill_json.extend([cur_level, from_level, to_level, percentage, training_time, time_to_complete, date_completed])
        mimetype = 'application/json'
        results.append(skill_json)
        data = json.dumps(results)
        return HttpResponse(data, mimetype)







def skillplanner(request):
    try:
        request.session['training_queue'] = TrainingQueue.objects.get(char_id=request.session['char_id'])
        return render(request, 'skillplanner.html', {'training_queue' : request.session['training_queue'] })
    except ObjectDoesNotExist:
        request.session['training_queue'] = []
        return render(request, 'skillplanner.html')

