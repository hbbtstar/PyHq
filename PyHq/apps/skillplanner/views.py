from django.shortcuts import render
from PyHq.apps.characterscreen.models import Skill, SkillGroup, RequiredSkill
import json
from django.http import HttpResponse

# Create your views here.
def get_skills(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        skills = Skill.objects.filter(name__icontains=q)
        print skills
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
    x = 1
    if x == 1:
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


def skillplanner(request):
    return render(request, 'skillplanner.html')

