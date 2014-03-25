import evelink
from PyHq.apps.characterscreen.models import Skill, SkillGroup, RequiredSkill

# kinda klunky, but walks through skill tree dicts to get name for skill id that current_training returns
def getSkillName(skill_tree, type_id):
    for k, v in skill_tree.iteritems():
        if k == type_id:
            return v['name']
        elif isinstance(v, dict):
            for k1, v1 in v.iteritems():
                if k1 == type_id:
                    return v1['name']
                elif isinstance(v1, dict):
                    for k2, v2 in v1.iteritems():
                        if k2 == type_id:
                            return v2['name']


def EveSkillsToDB():
    eve_api = evelink.eve.EVE()
    eve_skill_tree = eve_api.skill_tree().result
    for k, v in eve_skill_tree.iteritems():
        g = SkillGroup(skill_group_id=k, name=v['name'])
        for k2, v2 in v['skills'].iteritems():
            skill_insert = Skill(skill_id=v2['id'], name=v2['name'], description=v2['description'], rank=v2['rank'])
            for k3, v3 in v2['required_skills'].iteritems():
                skill_required = RequiredSkill(skill_id=v2['id'], required_id=v3['id'],
                                               required_level=v3['level'])
                skill_required.save()
                # PUT BONUSES HERE
            skill_insert.primaryAttribute = v2['attributes']['primary']
            skill_insert.secondaryAttribute = v2['attributes']['secondary']
        skill_insert.save()
        g.save()
    return








