from django.db import models

# Create your models here.

class Character(models.Model):
    char_id = models.IntegerField()
    name = models.CharField(max_length=200)
    corporation = models.CharField(max_length=200)
    wallet_balance = models.FloatField()
    skill_points_total = models.FloatField()
    charisma = models.IntegerField()
    intelligence = models.IntegerField()
    perception = models.IntegerField()
    memory = models.IntegerField()
    willpower = models.IntegerField()

class Account(models.Model):
    v_code = models.CharField(max_length=200)
    key_id = models.CharField(max_length=200)