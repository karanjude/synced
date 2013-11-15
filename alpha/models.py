import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'synced.settings'

import sys
sys.path.append("../..")


from django.db import models



# Create your models here.
class FBUser(models.Model):
    id = models.IntegerField(default=0,primary_key=True)
    name = models.CharField(max_length=100)
    link = models.CharField(max_length=150)
    gender=models.CharField(max_length=6)
    locale=models.CharField(max_length=6)
    access_token = models.CharField(max_length=250)
    token_expired = models.BooleanField(default = False)

    def __str__(self):
        return "%s %s" % (self.id, self.name)


class FBFriend(models.Model):
    friend_of = models.ForeignKey(FBUser)
    id = models.IntegerField(default=0,primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return "%s %s" % (self.id, self.name)
