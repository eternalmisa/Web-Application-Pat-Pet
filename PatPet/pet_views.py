from django.http import Http404
from django.contrib.auth.models import User
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.conf import settings
from PatPet.models import *
from PatPet.forms import *
from mimetypes import guess_type
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from PatPet.util import format_address_helper


@login_required
def add_pet(request):
    context = {}
    if request.user.is_authenticated():
        context['isLogin'] = 1
    else:
        context['isLogin'] = 0
    if request.method == 'GET':
        context['PetBasicForm'] = PetBasicForm()
        context['PetLocationForm'] = PetLocationForm()
        context['PetMediaForm'] = PetMediaForm()
        return render(request, 'PatPet/add-pet.html', context)

    form1 = PetBasicForm(request.POST, request.FILES)
    form2 = PetLocationForm(request.POST)
    form3 = PetMediaForm(request.POST, request.FILES)
    context['PetBasicForm'] = form1
    context['PetLocationForm'] = form2
    context['PetMediaForm'] = form3

    if not form1.is_valid():
        return render(request, 'PatPet/add-pet.html', context)
    if not form2.is_valid():
        return render(request, 'PatPet/add-pet.html', context)
    if not form3.is_valid():
        return render(request, 'PatPet/add-pet.html', context)
    list = format_address_helper(form2.cleaned_data['pet_address'], form2.cleaned_data['pet_city'],
                                 form2.cleaned_data['pet_state'])

    pet_info = PetInfo.objects.create(owner=request.user,
                                      name=form1.cleaned_data['name'],
                                      age=form1.cleaned_data['age'],
                                      gender=form1.cleaned_data['gender'],
                                      breed=form1.cleaned_data['breed'],
                                      color=form1.cleaned_data['color'],
                                      pet_state=form2.cleaned_data['pet_state'],
                                      pet_city=form2.cleaned_data['pet_city'],
                                      pet_address=form2.cleaned_data['pet_address'],
                                      pet_zipcode=form2.cleaned_data['pet_zipcode'],
                                      pet_bio=form1.cleaned_data['pet_bio'], latitude=list[0], longitude=list[1])

    pet_info.save()

    if form1.cleaned_data['pet_avatar'] != None:
        pet_info.pet_avatar=form1.cleaned_data['pet_avatar']
    pet_info.save()

    for f in form3.cleaned_data['pet_photo']:
        a_photo = PetPhoto(pet_photo=f, pet_album=pet_info)
        a_photo.save()

    for g in form3.cleaned_data['pet_video']:
        a_video = PetVideo(pet_video=g, pet_videoSet=pet_info)
        a_video.save()
    return redirect(reverse('pet_profile', args=(pet_info.id,)))


@login_required
def delete_pet(request, pid):
    try:
        pet = get_object_or_404(PetInfo,pk=pid)
    except PetInfo.DoesNotExist:
        return HttpResponse("No such pet!")
    pet.delete()
    return redirect('/myprofile')


# delete photo: 0 for petprofile, 1 for renter_transaction, 2 for owner_transaction
@login_required
def delete_photo(request, index, pid):
    if int(index) == 0:
        try:
            photo = get_object_or_404(PetPhoto,pk=pid)
            pet = photo.pet_album
        except PetInfo.DoesNotExist:
            return HttpResponse("No such photo!")
        photo.pet_photo.delete()
        return redirect(reverse('pet_profile', args=(pet.id,)))
    elif int(index) == 1:
        try:
            photo = get_object_or_404(MomentPhoto,pk=pid)
            moment = photo.moment_album
            activity = moment.moment
        except Activity.DoesNotExist:
            return HttpResponse("No such photo!")
        photo.delete()
        return redirect(reverse('transaction_renter', args=(activity.id,)))
    else:
        try:
            photo = get_object_or_404(MomentPhoto,pk=pid)
            moment = photo.moment_album
            activity = moment.moment
        except Activity.DoesNotExist:
            return HttpResponse("No such photo!")
        photo.delete()
        return redirect(reverse('transaction_owner', args=(activity.id,)))


@login_required
def delete_video(request, index, vid):
    if int(index) == 0:
        try:
            video = get_object_or_404(PetVideo,pk=vid)
            pet = video.pet_videoSet
        except PetInfo.DoesNotExist:
            return HttpResponse("No such video!")
        video.pet_video.delete()
        video.delete()
        return redirect(reverse('pet_profile', args=(pet.id,)))
    elif int(index) == 1:
        try:
            video = get_object_or_404(MomentVideo,pk=vid)
            moment = video.moment_videoSet
            activity = moment.moment
        except Activity.DoesNotExist:
            return HttpResponse("No such video!")
        video.delete()
        return redirect(reverse('transaction_renter', args=(activity.id,)))
    else:
        try:
            video = get_object_or_404(MomentVideo,pk=vid)
            moment = video.moment_videoSet
            activity = moment.moment
        except Activity.DoesNotExist:
            return HttpResponse("No such video!")
        video.delete()
        return redirect(reverse('transaction_owner', args=(activity.id,)))


def pet_profile(request, pid):
    context = {}
    context['STATIC_URL'] = '/static/'
    context['MEDIA_URL'] = '/media/'
    #transactions = []
    if request.user.is_authenticated():
        context['isLogin'] = 1
    else:
        context['isLogin'] = 0
    pet = get_object_or_404(PetInfo, pk=pid)
    ##rating
    reviews = pet.pet_reviews.all()
    reviews_num = len(reviews)
    context['reviews_num']=reviews_num
    context['rating']=pet.pet_rating
<<<<<<< HEAD
=======
    print "dfajdhfkjadhfjkahdfk",pid

    # for transaction in Activity.objects.filter(pk__exact=pid):
    #     transactions.append(transaction)
>>>>>>> e02b2c7f8a09ad9cb9d33d629913ec46e93def55
    transactions=pet.pet.all()
    context['viewed_times']=pet.viewed_times
    context['reviews'] = reviews
    context['transactions'] = transactions
    context['pet'] = pet
    context['pet_owner'] = pet.owner
    context['pet_owner_info'] = pet.owner.person_info
    photos = pet.petInfo_photos.all()
    videos = pet.petInfo_videos.all()
    context['photos'] = photos
    context['videos'] = videos
    context['PetBasicForm'] = PetBasicForm(
        initial={'breed': pet.breed, 'gender': pet.gender, 'age': pet.age, 'color': pet.color, 'pet_bio': pet.pet_bio})
    context['PetLocationForm'] = PetLocationForm(
        initial={'pet_address': pet.pet_address, 'pet_city': pet.pet_city, 'pet_state': pet.pet_state,
                 'pet_zipcode': pet.pet_zipcode})

    if request.method == "GET":
        pet.viewed_times=pet.viewed_times+1
        pet.save()
        context['viewed_times']=pet.viewed_times
        return render(request, 'PatPet/pet-profile.html', context)

    if request.method == "POST" and 'basic' in request.POST:
        form = PetBasicForm(request.POST)
        context['PetBasicForm'] = form

        if not form.is_valid():
            context["error_flag"] = 1
            return render(request, 'PatPet/pet-profile.html', context)

        pet.breed = form.cleaned_data['breed']
        pet.gender = form.cleaned_data['gender']
        pet.color = form.cleaned_data['color']
        pet.age = form.cleaned_data['age']
        pet.pet_bio = form.cleaned_data['pet_bio']
        pet.save()
        return render(request, 'PatPet/pet-profile.html', context)

    if request.method == "POST" and 'avatar' in request.POST:
        if not request.FILES.get('img' ''):
            return render(request, 'PatPet/pet-profile.html', context)
        pet.pet_avatar = request.FILES.get('img' '')
        pet.save()
        return render(request, 'PatPet/pet-profile.html', context)

    if request.method == "POST" and 'media' in request.POST:
        form2 = PetMediaForm(request.POST, request.FILES)
        context['PetMediaForm'] = form2
        if not form2.is_valid():
            return render(request, 'PatPet/pet-profile.html', context)

        for f in form2.cleaned_data['pet_photo']:
            a_photo = PetPhoto(pet_photo=f, pet_album=pet)
            a_photo.save()
        for g in form2.cleaned_data['pet_video']:
            a_video = PetVideo(pet_video=g, pet_videoSet=pet)
            a_video.save()
        return render(request, 'PatPet/pet-profile.html', context)

    if request.method == "POST" and 'location' in request.POST:
        form3 = PetLocationForm(request.POST)
        context['PetLocationForm'] = form3
        if not form3.is_valid():
            context["error_flag2"] = 1
            return render(request, 'PatPet/pet-profile.html', context)
        pet.pet_state = form3.cleaned_data['pet_state']
        pet.pet_city = form3.cleaned_data['pet_city']
        pet.pet_address = form3.cleaned_data['pet_address']
        pet.pet_zipcode = form3.cleaned_data['pet_zipcode']
        list = format_address_helper(form3.cleaned_data['pet_address'], form3.cleaned_data['pet_city'],
                                     form3.cleaned_data['pet_state'])
        pet.latitude = list[0]
        pet.longitude = list[1]
        pet.save()
        context['pet'] = pet
        return render(request, 'PatPet/pet-profile.html', context)
