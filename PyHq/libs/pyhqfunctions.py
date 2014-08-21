import evelink
import json,requests
from PyHq.apps.characterscreen.models import *

# kinda klunky, but walks through skill tree dicts to get name for skill id that current_training returns
# OB-SO_LEEET since everything was moved to models, much faster and easier to work with now
# def getSkillName(skill_tree, type_id):
#     for k, v in skill_tree.iteritems():
#         if k == type_id:
#             return v['name']
#         elif isinstance(v, dict):
#             for k1, v1 in v.iteritems():
#                 if k1 == type_id:
#                     return v1['name']
#                 elif isinstance(v1, dict):
#                     for k2, v2 in v1.iteritems():
#                         if k2 == type_id:
#                             return v2['name']


def EveSkillsToDB():
    eve_api = evelink.eve.EVE()
    eve_skill_tree = eve_api.skill_tree().result
    for k, v in eve_skill_tree.iteritems():
        print(k, v['name'])
        g = SkillGroup(skill_group_id=k, name=v['name'])
        for k2, v2 in v['skills'].iteritems():
            skill_insert = Skill(skill_id=v2['id'], name=v2['name'], description=v2['description'], rank=v2['rank'],

                                    group_id=k)
            for k3, v3 in v2['required_skills'].iteritems():
                skill_required = RequiredSkill(from_skill_id=v2['id'], required_id=v3['id'],
                                               required_level=v3['level'])
                skill_required.save()
                # PUT BONUSES HERE

            skill_insert.primaryAttribute = v2['attributes']['primary']
            skill_insert.secondaryAttribute = v2['attributes']['secondary']
            print(k2, v2['name'])
            skill_insert.save()
        g.save()
    return

def CreateChar(char_id, api, Account):
    char = evelink.char.Char(char_id=char_id, api=api)
    char_standings = char.standings().result
    char_sheet = char.character_sheet().result
    char_update = Character(id=char_id, name=char_sheet['name'],
                           race=char_sheet['race'],
                           bloodline=char_sheet['bloodline'],
                           ancestry=char_sheet['ancestry'],
                           skill_points=char_sheet['skillpoints'],
                           skills=char_sheet['skills'],
                           account_id=Account, attributes=char_sheet['attributes'],
                           standings=char_standings, balance=char_sheet['balance'],
                           skill_queue=char.skill_queue().result,
                           current_training=char.current_training().result,
                           clone=char_sheet['clone'], corp=char_sheet['corp'])
    char_update.save()

def UpdateChar(char_id, api):
    char = evelink.char.Char(char_id=char_id, api=api)
    char_standings = char.standings().result
    char_sheet = char.character_sheet().result
    char_update = Character.objects.get(id=char_id)
    char_update.skills = char_sheet['skills']
    char_update.skill_points = char_sheet['skillpoints']
    char_update.attributes = char_sheet['attributes']
    char_update.standings = char_standings
    char_update.balance = char_sheet['balance']
    char_update.skill_queue = char.skill_queue().result
    char_update.current_training = char.current_training().result
    char_update.clone = char_sheet['clone']
    char_update.corp = char_sheet['corp']
    char_update.save()



def SpPerHour(primary_attribute, secondary_attribute):
    # figure out how long a skill will take to train based on given character
    return

def get_best_order(type_id, region_id, buy_sell, solar_system_ids="0"):
    # TODO: get best order for given function (highest for buy, lowest for sell)
    return


def get_price(type_ids, region_ids=None, buy_sell="b", solar_system_ids=None):
    # get average price over 24 hours for given items
    url = "http://api.eve-marketdata.com/api/item_prices2.json?char_name=demo&type_ids="
    url += ','.join(type_ids)
    url += "&region_ids="
    url += ','.join(region_ids)
    url += "&solarsystem_ids="
    url += ",".join(solar_system_ids)
    url += "&buy_sell="
    url += buy_sell
    r = requests.get(url)
    return r.json()











