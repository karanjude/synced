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
        if f.access_token is None:
            f.access_token = a_token

    except Exception as e:
        f = FBUser(id = u_id, access_token = a_token)

    f.save()


if __name__ == "__main__":
    register("635875436","CAAFMEslK1gcBANx6HpVHLCZBpRkIZBENr23aAIPetf3rcqdh4UWlR5jqDlZCMbFIXJvzz2c0RW0DyDwOpGTKifVto11i0gnhmZBflYlPzdTMIWh0rAWydVQjyqB1FvpYZCUaEZAxwXtJZBQ2xZAHpf1RLQa3tRZAMmTtKCqN6FkvY1Y2A6gDb82LpFHhghGAdWdkZD")

