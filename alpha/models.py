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

    def has_access_token(self):
        return self.access_tokenis is not None

    def __str__(self):
        return unicode("%s %s" % (self.id, self.name))


class FBFriend(models.Model):
    friend_of = models.ForeignKey(FBUser)
    id = models.IntegerField(default=0,primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return unicode("Friend %s %s" % (self.id, self.name))

class UserProcessed(models.Model):
    processed_for = models.ForeignKey(FBUser)
    profile_processed = models.BooleanField(default=False)
    friends_processed = models.BooleanField(default=False)
    photos_processed = models.BooleanField(default=False)
    
class FBPhoto(models.Model):
    processed_for = models.ForeignKey(FBUser)
    photo_url = models.CharField(max_length=150)
