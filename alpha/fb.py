import sys

path = '/home/ubuntu/synced'

if path not in sys.path:
    sys.path.append(path)

import simplejson as json
import urllib

from alpha.models import FBUser, FBFriend

def register(u_id, a_token):
    try:
        f = FBUser.objects.get(pk = u_id)
        print "%s found, updating access_token %s" % (u_id, a_token)
        f.access_token = a_token

    except Exception as e:
        f = FBUser(id = u_id, access_token = a_token)

    f.save()


def update(u_id):
    try:
        f = FBUser.objects.get(pk = u_id)
        print "%s found, updating user details " % (u_id)

        url = "https://graph.facebook.com/" + str(f.id) + "?access_token=" + f.access_token
        print "calling url " + url

        usr_json = urllib.urlopen(url).read()
        usr_obj = json.loads(usr_json)

        print "usr obj %s" % (usr_obj)
        
        f.name = usr_obj["name"]
        f.link = usr_obj["link"]
        f.gender = usr_obj["gender"]
        f.locale = usr_obj["locale"]

        print "About to save usr ", f

        f.save()

        print "usr saved ", f
    except Exception as e:
        print e


if __name__ == "__main__":
    #register("635875436","CAAFMEslK1gcBANx6HpVHLCZBpRkIZBENr23aAIPetf3rcqdh4UWlR5jqDlZCMbFIXJvzz2c0RW0DyDwOpGTKifVto11i0gnhmZBflYlPzdTMIWh0rAWydVQjyqB1FvpYZCUaEZAxwXtJZBQ2xZAHpf1RLQa3tRZAMmTtKCqN6FkvY1Y2A6gDb82LpFHhghGAdWdkZD")

    update("635875436")

