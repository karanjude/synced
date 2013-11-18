# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.shortcuts import render_to_response
from django.core.context_processors import csrf

from alpha.models import FBUser, FBFriend
import fb


def index(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('home.html',c)


def register(request):
    access_token = request.REQUEST["a_token"]
    user_id = request.REQUEST["u_id"]
    
    print access_token, user_id

    fb.register(user_id, access_token)
    fb.update_user(user_id)

    return HttpResponse(request.REQUEST["u_id"])

