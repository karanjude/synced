# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.forms.models import model_to_dict

import simplejson as json

from alpha.models import FBUser, FBFriend
import fb


def index(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('home.html',c)

def synced(request):
    c = {}
    c.update(csrf(request))
    c["user_id"] = request.REQUEST["uid"]
    return render_to_response('synced.html',c)

def syncedprogress(request):
    u_id = request.REQUEST["u_id"]
    response_data = {}

    p = fb.get_processed_object(u_id)
    if p is not None:
        response_data["progress"] = model_to_dict(p)
    else:
        response_data["progress"] = {}


    return HttpResponse(json.dumps(response_data), content_type="application/json")


def register(request):
    access_token = request.REQUEST["a_token"]
    user_id = request.REQUEST["u_id"]
    
    print access_token, user_id

    fb.register(user_id, access_token)
    fb.update_user(user_id)

    return HttpResponse(request.REQUEST["u_id"])

