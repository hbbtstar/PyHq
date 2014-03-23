import evelink
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


