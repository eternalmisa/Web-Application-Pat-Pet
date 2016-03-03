from django.http import Http404
from django.contrib.auth.models import User
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from PatPet.models import *
from PatPet.forms import *
from mimetypes import guess_type
from django.core.urlresolvers import reverse
import json
from django.http import HttpResponse
from django.db.models import Q

@login_required
def myprofile(request):
    context = {}
    context['STATIC_URL'] = '/static/'
    context['MEDIA_URL'] = '/media/'

    if request.user.is_authenticated():
        context['isLogin'] = 1
    else:
        context['isLogin'] = 0
    user = request.user
    info = PersonInfo.objects.get(user=request.user)

    petlist = []
    reviews = info.person_reviews.all()
    context['rating'] = info.rating
    context['reviews_num'] = len(reviews)
    reviews_as_owner = []
    reviews_as_renter = []
    pets = PetInfo.objects.all()
    for review in reviews:
        if review.activity.owner == info:
            reviews_as_owner.append(review)
        if review.activity.renter == info:
            reviews_as_renter.append(review)
    context['reviews_as_owner'] = reviews_as_owner
    context['reviews_as_renter'] = reviews_as_renter
    for pet in pets:
        if pet.owner == user:
            petlist.append(pet)

    transactions = Activity.objects.filter(
        Q(owner=user.person_info) | Q(renter=user.person_info))

    context['transactions'] = transactions
    context['info'] = info
    context['petlist'] = petlist
    return render(request, 'PatPet/person-profile.html', context)


def person_profile(request, uid):
    context = {}
    if request.user.is_authenticated():
        context['isLogin'] = 1
    else:
        context['isLogin'] = 0
    user =  get_object_or_404(User,pk=uid)
    info = PersonInfo.objects.get(user__exact=user)
    petlist = []
    pets = PetInfo.objects.all()
    reviews = info.person_reviews.all()
    reviews_num = len(reviews)
    context['rating'] = info.rating
    context['reviews_num'] = reviews_num
    reviews_as_owner = []
    reviews_as_renter = []
    for review in reviews:
        if review.activity.owner == info:
            reviews_as_owner.append(review)
        if review.activity.renter == info:
            reviews_as_renter.append(review)
    context['reviews_as_owner'] = reviews_as_owner
    context['reviews_as_renter'] = reviews_as_renter
    for pet in pets:
        if pet.owner == user:
            petlist.append(pet)

    transactions = Activity.objects.filter(
        Q(owner=user.person_info) | Q(renter=user.person_info))

    context['transactions'] = transactions

    context['info'] = info
    context['petlist'] = petlist
    context['STATIC_URL'] = '/static/'
    context['MEDIA_URL'] = '/media/'
    return render(request, 'PatPet/person-profile.html', context)


@login_required
def edit_profile(request):
    context = {}
    if request.user.is_authenticated():
        context['isLogin'] = 1
    else:
        context['isLogin'] = 0
    user = request.user
    info = PersonInfo.objects.get(user__exact=user)

    if request.method == 'GET':
        context['EditPersonInfoForm'] = EditPersonInfoForm(
            initial={'state': info.state, 'city': info.city, 'phoneNum': info.phoneNum, 'zipcode': info.zipcode,
                     'person_bio': info.person_bio, 'address': info.address, 'gender': info.gender,
                     'birthday': info.birthday})
        context['EditUserForm'] = EditUserForm(
            initial={'username': request.user.username, 'first_name': request.user.first_name,
                     'last_name': request.user.last_name})
        return render(request, 'PatPet/edit-profile.html', context)

    form1 = EditPersonInfoForm(request.POST, request.FILES)
    form2 = EditUserForm(request.POST)
    context['EditPersonInfoForm'] = form1
    context['EditUserForm'] = form2
    context['info'] = info

    if not form1.is_valid() or not form2.is_valid():
        return render(request, 'PatPet/edit-profile.html', context)

    info.person_avatar = info.person_avatar
    info.state = form1.cleaned_data['state']
    info.city = form1.cleaned_data['city']
    info.zipcode = form1.cleaned_data['zipcode']
    info.address = form1.cleaned_data['address']
    info.gender = form1.cleaned_data['gender']
    info.phoneNum = form1.cleaned_data['phoneNum']
    info.birthday = form1.cleaned_data['birthday']
    info.person_bio = form1.cleaned_data['person_bio']

    if request.FILES.get('avatar',''):
        info.is_third = "0"
        info.person_avatar = request.FILES.get('avatar','')
    elif request.FILES.has_key('upload'):
        info.is_third = "0"
        info.person_avatar = request.FILES.get('upload' '')
    info.save()

    request.user.username = form2.cleaned_data['username']
    request.user.last_name = form2.cleaned_data['last_name']
    request.user.first_name = form2.cleaned_data['first_name']
    request.user.save()
    return HttpResponse("EditSuccess")
