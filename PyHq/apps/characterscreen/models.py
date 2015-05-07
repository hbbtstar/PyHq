# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `` lines for those models you wish to give write DB access
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from django.db import models
from django.contrib.auth.models import User
from picklefield.fields import PickledObjectField

class Account(models.Model):
    v_code = models.CharField(max_length=200)
    key_id = models.CharField(max_length=200)
    user = models.ForeignKey(User)

class Skill(models.Model):
    skill_id = models.IntegerField(primary_key=True)
    group_id = models.IntegerField()
    name = models.CharField(max_length=100)
    description = models.TextField()
    rank = models.IntegerField()
    primaryAttribute = models.CharField(max_length=20, null=True)
    secondaryAttribute = models.CharField(max_length=20, null=True)

    def __str__(self):
        return "{}".format(self.name)

class SkillGroup(models.Model):
    skill_group_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length="100")

    def __str__(self):
        return "{}".format(self.name)

class RequiredSkill(models.Model):
    id = models.AutoField(primary_key=True)
    from_skill_id = models.IntegerField()
    required_id = models.IntegerField()
    required_level = models.IntegerField()


class Character(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    race = models.CharField(max_length=50)
    ancestry = models.CharField(max_length=100)
    bloodline = models.CharField(max_length=100)
    skill_points = models.IntegerField()
    balance = models.BigIntegerField()
    account_id = models.ForeignKey(Account, related_name='characters')
    attributes = PickledObjectField()
    skills = PickledObjectField()
    standings = PickledObjectField()
    current_training = PickledObjectField()
    skill_queue = PickledObjectField()
    corp = PickledObjectField()

    def __str__(self):
        return "".format(self.name)


class TrainingQueue(models.Model):
    char_id = models.IntegerField(primary_key=True)
    queue = PickledObjectField()

