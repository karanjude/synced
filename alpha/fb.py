import sys

path = '/home/ubuntu/synced'
if path not in sys.path:
    sys.path.append(path)

import simplejson as json
import urllib

from alpha.models import FBUser, FBFriend, UserProcessed

import beanstalkc

def register(u_id, a_token):
    try:
        f = FBUser.objects.get(pk = u_id)
        print "%s found, updating access_token %s" % (u_id, a_token)
        f.access_token = a_token

    except Exception as e:
        f = FBUser(id = u_id, access_token = a_token)

    f.save()

def send_msg(msg):
    c = beanstalkc.Connection(host='localhost', port=11300)
    msg = str(msg)
    print "sending msg : |%s|" %  (msg)
    c.put(msg)
    c.close()

def update_user(u_id):
    user_processed = get_processed_object(u_id)
    if user_processed is None:
        f = FBUser.objects.get(pk = u_id)
        user_processed = f.userprocessed_set.create()
        user_processed.save()

    if user_processed.profile_processed is False:
        msg = "%s %s" % ('update_user_profile',u_id)
        send_msg(msg)

    if user_processed.friends_processed is False:
        msg = "%s %s" % ('update_user_friends',u_id)
        send_msg(msg)

    if user_processed.photos_processed is False:
        msg = "%s %s" % ('update_user_photos',u_id)
        send_msg(msg)
            

def update_profile_for_friend(f, u_id):
    url = "https://graph.facebook.com/%s?access_token=%s" % (u_id, f.access_token)
    print "calling url " + url

    usr_json = urllib.urlopen(url).read()
    usr_obj = json.loads(usr_json)

    print "usr obj %s" % (usr_obj)
    
    if str(f.id) != usr_obj["id"]:
        f = FBUser(id = int(usr_obj["id"]))

    f.name = usr_obj["name"]
    f.link = usr_obj["link"]
    f.gender = usr_obj["gender"]
    f.locale = usr_obj["locale"]

    print ("About to save usr %s " % (f)).encode('utf-8')
    f.save()
    print ("usr saved %s" % (f)).encode('utf-8')


def update_profile(u_id):
    try:
        f = FBUser.objects.get(pk = u_id)
        print "%s found, updating user details " % (u_id)
        
        update_profile_for_friend(f, u_id)
    except Exception as e:
        print e

def get_processed_object(u_id):
    user_processed = UserProcessed.objects.filter(processed_for = u_id)
    if len(user_processed) == 1:
        return user_processed[0]

    return None

def process_user_profile(u_id):
    print "processing profile for user :" + u_id
    update_profile(u_id)

    user_processed = get_processed_object(u_id)
    if user_processed is not None:
        user_processed.profile_processed = True
        user_processed.save()


def process_user_photos(u_id):
    print "processing photos for user :" + u_id

def process_friend_for(f, url):
    print "calling url " + url

    usr_json = urllib.urlopen(url).read()
    friends_obj = json.loads(usr_json)

    print "usr obj %s" % (friends_obj)

    for friend in friends_obj["friends"]['data']:
        name_ = unicode(friend["name"])
        id_ = friend["id"]

        try:
            fr = f.fbfriend_set.create(name=name_, id =id_)
            print "About to save friend ", str(fr).encode('utf-8')
            f.save()
            print "friend saved ", str(fr).encode('utf-8')

            update_profile_for_friend(f, fr.id)
        except Exception as ee:
            print ee
            continue

    if friends_obj.has_key("next"):
        return friends_obj["next"]

    return None

def process_user_friends(u_id):
    print "procesing friends for user :" + u_id

    try:
        f = FBUser.objects.get(pk = u_id)
        print "%s found, updating friends " % (u_id)

        url = "https://graph.facebook.com/" + str(f.id) + "?access_token=" + f.access_token + "&fields=friends"

        next_url = url
        while next_url is not None:
            next_url = process_friend_for(f, url)

        user_processed = get_processed_object(u_id)
        if user_processed is not None:
            user_processed.friends_processed = True
            user_processed.save()

    except Exception as e:
        print e

if __name__ == "__main__":
    #register("635875436","CAAFMEslK1gcBANx6HpVHLCZBpRkIZBENr23aAIPetf3rcqdh4UWlR5jqDlZCMbFIXJvzz2c0RW0DyDwOpGTKifVto11i0gnhmZBflYlPzdTMIWh0rAWydVQjyqB1FvpYZCUaEZAxwXtJZBQ2xZAHpf1RLQa3tRZAMmTtKCqN6FkvY1Y2A6gDb82LpFHhghGAdWdkZD")

    #update_profile("635875436")
    process_user_friends("635875436")

