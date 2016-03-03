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
from django.db.models import Q
import json
from django.http import HttpResponse
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
import pytz
from pytz import timezone

### Transaction page ######
@login_required
def add_transaction(request, pid):
    new_pet = get_object_or_404(PetInfo,pk=pid)
    new_pet.save()
    renter = request.user
    owner = new_pet.owner
    new_owner = get_object_or_404(PersonInfo,user=owner)
    new_renter =get_object_or_404(PersonInfo,user=renter)

    new_status = Status(statusText="Incomplete", price=1.00)
    new_status.save()
    new_moment = Moment()
    new_moment.save()
    new_activity = Activity(owner=new_owner, renter=new_renter, pet=new_pet, status=new_status, moment=new_moment)
    new_activity.save()

    return redirect(reverse('myprofile'))


@login_required
def transaction_renter(request, tid):
    context = {}

    if request.user.is_authenticated():
        context['isLogin'] = 1
    else:
        context['isLogin'] = 0

    new_activity = get_object_or_404(Activity,pk=tid)
    context['activity'] = new_activity
    context['renter'] = new_activity.renter.user
    contents = new_activity.moment_contents.all()
    context['contents'] = contents
    context['photoForm'] = MomentPhotoForm()
    context['videoForm'] = MomentVideoForm()
    moment = new_activity.moment
    if moment == None:
        context['photos'] = "no"
        context['videos'] = "no"
    else:
        photos = moment.moment_photos.all()
        context['photos'] = photos
        videos = moment.moment_videos.all()
        context['videos'] = videos

    return render(request, 'PatPet/transaction-renter.html', context)


@login_required
def upload_moment_content(request,tid):
    if request.method == 'GET':
        return HttpResponse("Please add comments by POST method")
    if not 'content' in request.POST or not request.POST['content']:
        return HttpResponse("You need to say something.")
    activity = Activity.objects.get(id__exact=request.POST['tid'])
    new_moment=MomentContent(content=request.POST['content'],activity=activity)
    new_moment.save()
    return HttpResponse("success")


def getmoments(request,tid):
    try:
        activity = get_object_or_404(Activity,pk=tid)
    except Activity.DoesNotExist:
        return HttpResponse("No such transaction!")
    moments=activity.moment_contents.all()
    json={}
    json['moments']=[]
    eastern = timezone('US/Eastern')
    fmt = '%b. %d, %Y, %I:%M %p.'
    for moment in moments:
        m={}
        m['content']=moment.content
        loc_time = moment.timestamp.astimezone(eastern)
        m['timestamp']=loc_time.strftime(fmt)
        m['mid']=moment.id
        json['moments'].append(m)
    return JsonResponse(json)


def delete_moment(request, cid):
    try:
        moment_content=get_object_or_404(MomentContent,pk=cid)
        activity=moment_content.activity
    except Activity.DoesNotExist:
        return HttpResponse("No such content!")
    moment_content.delete()
    return HttpResponse(cid)


@login_required
def upload_transaction_images(request, tid):
    context = {}
    new_activity = get_object_or_404(Activity,pk=tid)
    context['renter'] = new_activity.renter.user
    context['activity'] = new_activity
    context['videoForm'] = MomentVideoForm()
    contents = new_activity.moment_contents.all()
    context['contents'] = contents
    if request.method == 'GET':
        print("get method")
        context['photoForm'] = MomentPhotoForm()
        return render(request, 'PatPet/transaction-renter.html', context)
    form1 = MomentPhotoForm(request.POST, request.FILES)
    context['photoForm'] = form1
    if not form1.is_valid():
        print("incorrect")
        return render(request, 'PatPet/transaction-renter.html', context)
    print("correct")
    moment = new_activity.moment
    if form1.cleaned_data['photos'][0] != None:
        print("hi")

        for g in form1.cleaned_data['photos']:
            a_photo = MomentPhoto(moment_photo=g, moment_album=moment)
            a_photo.save()
    photos = moment.moment_photos.all()
    videos = moment.moment_videos.all()
    context['videos'] = videos
    context['photos'] = photos
    return render(request, 'PatPet/transaction-renter.html', context)


@login_required
def upload_transaction_videos(request, tid):
    context = {}
    new_activity = get_object_or_404(Activity,pk=tid)
    context['activity'] = new_activity
    context['photoForm'] = MomentPhotoForm()
    context['renter'] = new_activity.renter.user
    contents = new_activity.moment_contents.all()
    context['contents'] = contents
    if request.method == 'GET':
        print("get method")
        context['videoForm'] = MomentVideoForm()
        return render(request, 'PatPet/transaction-renter.html', context)
    form2 = MomentVideoForm(request.POST, request.FILES)
    context['videoForm'] = form2
    if not form2.is_valid():
        print("incorrect")
        return render(request, 'PatPet/transaction-renter.html', context)
    print("correct")
    moment = new_activity.moment
    if form2.cleaned_data['videos'][0] != None:
        for g in form2.cleaned_data['videos']:
            a_video = MomentVideo(moment_video=g, moment_videoSet=moment)
            a_video.save()
    photos = moment.moment_photos.all()
    videos = moment.moment_videos.all()
    context['videos'] = videos
    context['photos'] = photos
    return render(request, 'PatPet/transaction-renter.html', context)


@login_required
def transaction_owner(request, tid):
    context = {}
    if request.user.is_authenticated():
        context['isLogin'] = 1
    else:
        context['isLogin'] = 0
    new_activity =  get_object_or_404(Activity,pk=tid)
    context['activity'] = new_activity
    renter = new_activity.renter.user
    context['renter'] = renter
    contents = new_activity.moment_contents.all()
    context['contents'] = contents
    moment = new_activity.moment
    if moment == None:
        print  "no"
        context['photos'] = "no"
        context['videos'] = "no"
    else:
        print "yes"
        photos = moment.moment_photos.all()
        context['photos'] = photos
        videos = moment.moment_videos.all()
        context['videos'] = videos
    print "owner" + new_activity.renter.user.username
    print renter.id
    return render(request, 'PatPet/transaction-owner.html', context)


def transaction_visitor(request, tid):
    print("visitor2")
    context = {}
    new_activity = get_object_or_404(Activity,pk=tid)
    context['activity'] = new_activity
    renter = new_activity.renter.user
    context['renter'] = renter
    contents = new_activity.moment_contents.all()
    context['contents'] = contents
    moment = new_activity.moment
    if moment == None:
        print  "no"
        context['photos'] = "no"
        context['videos'] = "no"
    else:
        print "yes"
        photos = moment.moment_photos.all()
        context['photos'] = photos
        videos = moment.moment_videos.all()
        context['videos'] = videos
    print "owner" + new_activity.renter.user.username
    print renter.id
    return render(request, 'PatPet/transaction-visitor.html', context)


def transaction_view(request, tid, status, args):
    context = {}
    new_activity = get_object_or_404(Activity,pk=tid)
    context['activity'] = new_activity
    renter = new_activity.renter.user
    context['renter'] = renter
    contents = new_activity.moment_contents.all()
    context['contents'] = contents
    context['videoForm'] = MomentVideoForm()
    context['photoForm'] = MomentPhotoForm()
    moment = new_activity.moment
    if moment == None:
        print  "no"
        context['photos'] = "no"
        context['videos'] = "no"
    else:
        print "yes"
        photos = moment.moment_photos.all()
        context['photos'] = photos
        videos = moment.moment_videos.all()
        context['videos'] = videos
    for key in args.keys():
        context[key] = args[key]
    if status == 0:
        return render(request, 'PatPet/transaction-visitor.html', context)
    if status == 1:
        return render(request, 'PatPet/transaction-renter.html', context)
    if status == 2:
        return render(request, 'PatPet/transaction-owner.html', context)


def transaction(request, tid):
    new_activity = get_object_or_404(Activity,pk=tid)
    renter = new_activity.renter.user
    owner = new_activity.owner.user
    print("ok")
    print (request.user.username)

    if request.user.username == renter.username:
        return transaction_renter(request, tid)
    if request.user.username == owner.username:
        return transaction_owner(request, tid)
    else:
        print("visitor1")
        return transaction_visitor(request, tid)


@login_required
def renter_submit_review(request, tid):
    print ("test_submit")
    context = {}
    errors = []
    messages = []
    context['errors'] = errors
    activity = get_object_or_404(Activity,pk=tid)
    review_pet_text = request.POST['review_pet']
    review_pet_text=review_pet_text.strip()
    review_owner_text = request.POST['review_owner']
    review_owner_text=review_owner_text.strip()
    pet_rating = request.POST['pet_rating']
    owner_rating = request.POST['owner_rating']
    print pet_rating, "&&*****"
    ## pet
    if review_pet_text != '' and pet_rating != '':
        review_pet_rating = int(pet_rating)
        review_pet = ReviewPet(commenter=request.user, pet=activity.pet, content=review_pet_text,
                               grade_pet=review_pet_rating, activity=activity)
        review_pet.save()
        pet=review_pet.pet
        reviews = pet.pet_reviews.all()
        reviews_num = len(reviews)
        print "len",reviews_num
        sum = 0;
        if reviews_num != 0:
            for review in reviews:
                sum = sum + review.grade_pet
                print "sum",sum
            rating = round(float(sum) / float(reviews_num),1)
            pet.pet_rating=rating
            pet.save()
        else:
            rating=0
            pet.pet_rating=rating
            pet.save()
        print pet.pet_rating,"%%%%%%%%"
    elif review_pet_text != '' and pet_rating == '':
        errors.append("You must rating the pet")
        return transaction_view(request, tid, 1, context)
    elif review_pet_text == '' and pet_rating != '':
        errors.append("You must review the pet")
        return transaction_view(request, tid, 1, context)

    ## owner
    if review_owner_text != "" and owner_rating != "":
        review_owner_rating = int(owner_rating)
        review_owner = ReviewPerson(commenter=request.user, person=activity.owner, content=review_owner_text,
                                    grade_person=review_owner_rating, activity=activity)
        review_owner.save()
        owner=review_owner.person
        reviews=owner.person_reviews.all()
        reviews_num=len(reviews)
        print reviews_num,"hahaha"
        sum=0
        if reviews_num != 0:
            for review in reviews:
                sum = sum + review.grade_person
                print "sum",sum
            rating = round(float(sum) / float(reviews_num),1)
            owner.rating=rating
            owner.save()
        else:
            rating=0
            owner.rating=rating
            owner.save()
    elif review_owner_text == "" and owner_rating != "":
        errors.append("You must review the owner")
        return transaction_view(request, tid, 1, context)
    elif review_owner_text != "" and owner_rating == "":
        errors.append("You must rating the owner")
        return transaction_view(request, tid, 1, context)
    if review_owner_text == "" and owner_rating == "" and review_pet_text == "" and pet_rating == "":
        errors.append("You must submit something!")
        return transaction_view(request, tid, 1, context)
    messages.append("you have successfully submitted your reviews and ratings!")
    context["messages"] = messages
    return transaction_view(request, tid, 1, context)


@login_required
def owner_submit_review(request, tid):
    errors = []
    messages = []
    context = {}
    context['errors'] = errors
    context['messages'] = messages
    activity = get_object_or_404(Activity,pk=tid)
    review_renter_text = request.POST['review_renter']
    review_renter_text=review_renter_text.strip()
    #owner_rating = request.POST['owner_rating']
    renter_rating = request.POST['renter_rating']
    print review_renter_text
    if review_renter_text != "" and renter_rating != "":
        review_renter_rating = int(renter_rating)
        review_renter = ReviewPerson(commenter=request.user, person=activity.renter, content=review_renter_text,
                                     grade_person=review_renter_rating, activity=activity)
        review_renter.save()
        renter=review_renter.person
        reviews=renter.person_reviews.all()
        reviews_num=len(reviews)
        print reviews_num,"hahaha"
        sum = 0
        if reviews_num != 0:
            for review in reviews:
                sum = sum + review.grade_person
                print "sum",sum
            rating = round(float(sum) / float(reviews_num),1)
            renter.rating=rating
            renter.save()
        else:
            rating=0
            renter.rating=rating
            renter.save()
    elif review_renter_text == "" and renter_rating != "":
        errors.append("You must review the renter")
        return transaction_view(request, tid, 2, context)
    elif review_renter_text != "" and renter_rating == "":
        errors.append("You must rating the renter")
        print "error"
        return transaction_view(request, tid, 2, context)
    elif review_renter_text == "" and renter_rating == "":
        errors.append("You must submit something")
        return transaction_view(request, tid, 2, context)
    messages.append("You have submitted you reviews and ratings sucessfully")
    return transaction_view(request, tid, 2, context)
