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

def skillplanner(request):
    return render(request, 'skillplanner.html')

