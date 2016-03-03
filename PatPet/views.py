from django.http import Http404
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth import login, authenticate
from PatPet.models import *
from PatPet.forms import *
from django.core.urlresolvers import reverse
import hashlib, random
from django.utils import timezone
import re
from haystack.generic_views import SearchView
import json
from django.http import HttpResponse
from haystack.query import SearchQuerySet


def autocomplete(request):
    sqs = SearchQuerySet().autocomplete(content_auto=request.GET.get('q', ''))[:5]
    print("Auto complete")
    suggestions = [result.breed for result in sqs]
    # Make sure you return a JSON object, not a bare list.
    # Otherwise, you could be vulnerable to an XSS attack.
    the_data = json.dumps({
        'results': suggestions
    })
    return HttpResponse(the_data, content_type='application/json')


def index(request):
    context = {}
    pop_pets=[]
    top_pets=[]
    if request.user.is_authenticated():
        context['isLogin'] = 1
        if PersonInfo.objects.filter(pk=request.user.id).count() == 0:
            person_info = PersonInfo.objects.create(user=request.user, is_third="1")
            person_info.save()
    else:
        context['isLogin'] = 0
    context["bg_pic"] = []
    all_pets1 = PetInfo.objects.all().order_by("-pet_rating")
    if len(all_pets1)>=3:
        top_pets.append(all_pets1[0])
        top_pets.append(all_pets1[1])
        top_pets.append(all_pets1[2])
        context['top_pets']=top_pets
    else:
        context['top_pets']=all_pets1
    # rec_pets = PetInfo.objects.all()[:3]
    all_pets2=PetInfo.objects.all().order_by("-viewed_times")
    if len(all_pets2) >=3:
        pop_pets.append(all_pets2[0])
        pop_pets.append(all_pets2[1])
        pop_pets.append(all_pets2[2])
        context["pop_pets"] = pop_pets
    else:
        context['pop_pets']=all_pets2

    all_pets=PetInfo.objects.all()
    all_videos=[]
    if len(all_pets) !=0:
        for pet in all_pets:
            videos = pet.petInfo_videos.all()
            if len(videos) !=0:
                for video in videos:
                    all_videos.append(video.pet_video)


    all_activities=Activity.objects.all()
    if len(all_activities)!=0:
        for activity in all_activities:
            if len(activity.moment.moment_videos.all())!=0:
                for video in activity.moment.moment_videos.all():
                    all_videos.append(video.moment_video)
    print len(all_videos),"&&&&&"
    if len(all_videos)>=3:
        selected_videos=random.sample(all_videos,3)
        context['selected_videos']=selected_videos
    else:
        context['selected_videos']=all_videos

    form = DateRangeSearchForm()
    context['form'] = form
    return render(request, 'PatPet/index.html', context)


### Search page ######
class CustomSearchView(SearchView):
    """My custom search view."""
    template_name = 'search/search.html'
    # queryset = SearchQuerySet().filter(author='john')
    form_class = DateRangeSearchForm

    def get_queryset(self):
        print("get_queryset")
        queryset = super(CustomSearchView, self).get_queryset()
        print(queryset)
        # further filter queryset based on some set of criteria
        return queryset

    def get_context_data(self, *args, **kwargs):
        print("get_context_data")
        context = super(CustomSearchView, self).get_context_data(*args, **kwargs)
        print(type(context))
        if self.request.user.is_authenticated():
            context['isLogin'] = 1
        else:
            context['isLogin'] = 0
        # do something
        return context

