from django.http import Http404
from django.contrib.auth.models import User
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate

from django.contrib.auth import logout as auth_logout, login
from django.conf import settings
from PatPet.models import *
from PatPet.forms import *
from mimetypes import guess_type
from django.core.urlresolvers import reverse
from django.db.models import Q
import hashlib, random
from django.utils import timezone
from django.core.mail import send_mail
import re
import json
from django.http import HttpResponse


def logout(request):
    auth_logout(request)
    return redirect('/')

### sign up page ######
def gotosignup(request):
    context = {}
    if request.method == 'GET':
        context['SignUpForm1'] = SignUpForm1()
        context['SignUpForm2'] = SignUpForm2()
        return render(request, 'PatPet/sign-up.html', context)

    salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
    activation_key = hashlib.sha1(salt + request.POST['email']).hexdigest()
    key_expires = datetime.datetime.today() + datetime.timedelta(2)
    if User.objects.filter(username__exact=request.POST['username']):
        return HttpResponse("The username is already taken")

    new_user = User.objects.create_user(username=request.POST['username'],
                                        first_name=request.POST['firstname'],
                                        last_name=request.POST['lastname'],
                                        password=request.POST['password1'],
                                        email=request.POST['email'])
    new_user.is_active = False
    person_info = PersonInfo.objects.create(user=new_user,
                                            address=request.POST['address'],
                                            state=request.POST['state'],
                                            city=request.POST['city'],
                                            zipcode=request.POST['zipcode'],
                                            activation_key=activation_key,
                                            key_expires=key_expires)

    person_info.save()

    if request.FILES.get('avatar'):
        person_info.is_third = "0"
        person_info.person_avatar = request.FILES.get('avatar','')
    elif request.FILES.has_key('upload'):
        person_info.is_third = "0"
        file=request.FILES.get('upload' '')
        person_info.person_avatar = file

    person_info.save()
    email_subject = 'Account confirmation'
    email_body = "Hey %s, thanks for signing up. To activate your account, click this link within \
            48hours http://ec2-52-35-25-163.us-west-2.compute.amazonaws.com/accounts/confirm/%s" % (new_user.username, activation_key)
    send_mail(email_subject, email_body, settings.EMAIL_HOST_USER, [new_user.email], fail_silently=True)
    return HttpResponse("True")


def login_active(request):
    context={}
    context['go_active'] = True
    context['form'] = LoginForm()
    return render(request, 'PatPet/sign-in.html', context)


def active_account(request, activation_key):
    if request.user.is_authenticated():
        return redirect('/')
    user_profile = get_object_or_404(PersonInfo, activation_key=activation_key)
    if user_profile.key_expires < timezone.now():
        return HttpResponse("Activation faild, the activitaion has expired.")
    user = user_profile.user
    user.is_active = True
    user.save()
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)
    return redirect('/')


def checkUser(request):
    user = None
    if request.POST.has_key('name'):
        username = request.POST['name']
        result = {}
        user = User.objects.filter(username__exact=username)
    if user:
        result = """{"result":false}"""
    else:
        result = """{"result":true}"""
    return HttpResponse(result)

def checkUserForEdit(request):
    user = None
    if request.POST.has_key('name'):
        username = request.POST['name']
        result = {}
        users = User.objects.exclude(Q(pk=request.user.id))

    if username != request.user.username and len(User.objects.filter(username=username)) > 0:
        result = """{"result":false}"""
    else:
        result = """{"result":true}"""
    return HttpResponse(result)


def checkEmail(request):
    if request.POST.has_key('name'):
        email = request.POST['name']
        email = User.objects.filter(email__exact=email)
    if email:
        result = """{"result":false}"""
    else:
        result = """{"result":true}"""
    return HttpResponse(result)
