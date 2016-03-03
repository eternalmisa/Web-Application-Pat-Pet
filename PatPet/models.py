from django.db import models
from django.contrib.auth.models import User
import datetime
import random


def default_lat():
    return 40.443989 + random.uniform(-0.01, 0.01)


def default_lng():
    return -79.951847 + random.uniform(-0.01, 0.01)


def person_avatar_path(instance, filename):
    return 'persons/person_{0}/avatar/{1}'.format(instance.user.id, filename)


def pet_avatar_path(instance, filename):
    return 'pets/pet_{0}/avatar/{1}'.format(instance.id, filename)


def pet_photo_path(instance, filename):
    return 'pets/pet_{0}/photos/{1}'.format(instance.pet_album.id, filename)


def pet_video_path(instance, filename):
    return 'pets/pet_{0}/videos/{1}'.format(instance.pet_videoSet.id, filename)


def moment_photo_path(instance, filename):
    return 'transactions/transaction_{0}/photos/{1}'.format(instance.moment_album.id, filename)


def moment_video_path(instance, filename):
    return 'transactions/transaction_{0}/videos/{1}'.format(instance.moment_videoSet.id, filename)


## Pet Model ##
class PetInfo(models.Model):
    owner = models.ForeignKey(User, related_name="owner", null=True)
    name = models.CharField(max_length=30)
    age = models.IntegerField(default=0)
    gender = models.CharField(max_length=30)
    breed = models.CharField(max_length=30)
    color = models.CharField(max_length=30)
    pet_avatar = models.ImageField(upload_to=pet_avatar_path, default="../static/PatPet/images/pet-default-avatar.png")
    pet_rating = models.FloatField(default=0.0)
    pet_state = models.CharField(max_length=100)
    pet_city = models.CharField(max_length=100, default="Pittsburgh, PA, United States")
    pet_address = models.CharField(max_length=100)
    pet_zipcode = models.CharField(max_length=50, default="")
    pet_bio = models.CharField(max_length=100)
    viewed_times = models.IntegerField(default=0)
    flag = models.IntegerField(default=1)  # 0 is not avai, 1 is avai
    start_date = models.DateField(default=datetime.date.today)  # When will it be avai
    num_of_days = models.IntegerField(default=7)  # And avai for how many days?
    latitude = models.FloatField(default=default_lat)
    longitude = models.FloatField(default=default_lng)


class PetPhoto(models.Model):
    pet_photo = models.ImageField(upload_to=pet_photo_path, blank=True)
    pet_album = models.ForeignKey(PetInfo, related_name="petInfo_photos", null=True)


class PetVideo(models.Model):
    pet_video = models.FileField(upload_to=pet_video_path, blank=True)
    pet_videoSet = models.ForeignKey(PetInfo, related_name="petInfo_videos", null=True)


class Status(models.Model):
    statusText = models.CharField(max_length=30, default="")
    starttime = models.DateTimeField()
    endtime = models.DateTimeField()
    price = models.FloatField(default=0.0)


## Person Model ##
class PersonInfo(models.Model):
    person_avatar = models.ImageField(upload_to=person_avatar_path, default="../static/PatPet/images/default-avatar.png")
    state = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    address = models.CharField(max_length=50, blank=True)
    zipcode = models.CharField(max_length=50, default="")
    phoneNum = models.CharField(max_length=50, default="")
    person_bio = models.CharField(max_length=420, default="No instruction", blank=True)
    birthday = models.CharField(max_length=30, default='')
    gender = models.CharField(max_length=10, default='')
    rating = models.FloatField(default=0.0)
    user = models.OneToOneField(User, related_name="person_info")
    token = models.CharField(default="", max_length=50)
    latitude = models.FloatField(default=40.443989)
    longitude = models.FloatField(default=-79.941874)
    activation_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField(default=datetime.date.today())
    is_third = models.CharField(max_length=10, blank=True)


## Transaction ##
class Moment(models.Model):
    content = models.CharField(max_length=200, default="", blank=True, null=True)
    timestamp = models.DateTimeField(auto_now=True)


class Activity(models.Model):
    owner = models.ForeignKey(PersonInfo, related_name="seller")
    renter = models.ForeignKey(PersonInfo, related_name="buyer")
    pet = models.ForeignKey(PetInfo, related_name="pet")
    moment = models.OneToOneField(Moment, related_name="moment", null=True)
    status = models.OneToOneField(Status, related_name="status", null=True)


class MomentPhoto(models.Model):
    moment_photo = models.ImageField(upload_to=moment_photo_path, blank=True)
    moment_album = models.ForeignKey(Moment, related_name="moment_photos", null=True)


class MomentVideo(models.Model):
    moment_video = models.FileField(upload_to=moment_video_path, blank=True)
    moment_videoSet = models.ForeignKey(Moment, related_name="moment_videos", null=True)


class MomentContent(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=100)
    activity = models.ForeignKey(Activity, related_name="moment_contents")



class ReviewPet(models.Model):
    commenter = models.ForeignKey(User)
    pet = models.ForeignKey(PetInfo, related_name="pet_reviews")
    content = models.CharField(max_length=200, default="", blank=True)
    grade_pet = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    activity = models.ForeignKey(Activity, related_name="pet_reviews")


class ReviewPerson(models.Model):
    commenter = models.ForeignKey(User)
    person = models.ForeignKey(PersonInfo, related_name="person_reviews")
    content = models.CharField(max_length=200, default="", blank=True)
    grade_person = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    activity = models.ForeignKey(Activity, related_name="person_reviews")


## Chat ##
class Chat(models.Model):
    owner = models.OneToOneField(PersonInfo, related_name="chat_seller")
    renter = models.OneToOneField(PersonInfo, related_name="chat_buyer")
    pet = models.OneToOneField(PetInfo, related_name="chat_pet")
    starttime = models.DateTimeField(auto_now_add=True)
    endtime = models.DateTimeField(auto_now_add=True)


class ChatRoom(models.Model):
    chatId = models.CharField(max_length=60, blank=True)
    currenNumUser = models.IntegerField(default=0)


class ChatRoomUser(models.Model):
    name = models.CharField(max_length=20)
    room = models.ForeignKey(ChatRoom, related_name="chatRoom_users")


class UnreadMessages(models.Model):
    user = models.OneToOneField(User, unique=True)


class MessageChat(models.Model):
    messageDicts = models.ForeignKey(ChatRoom, related_name="chatRoom_messages", null=True)
    sendUser = models.ForeignKey(PersonInfo, related_name="send_user")
    messageContent = models.CharField(max_length=400, default="", blank=True)
    timestamp = models.DateTimeField(auto_now=True)
    messageType = models.CharField(max_length=10, default="", blank=True)
    petId = models.IntegerField(default=0)
    clickFlag = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s" % (self.messageContent)

    def __str__(self):
        return "%s" % (self.messageContent)


class MessageUnread(models.Model):
    messageDicts = models.ForeignKey(UnreadMessages, related_name="unreadmessages", null=True)
    sendUser = models.ForeignKey(PersonInfo, related_name="unread_send")
    messageContent = models.CharField(max_length=400, default="", blank=True)
    timestamp = models.DateTimeField(auto_now=True)


class PendingChatRoom(models.Model):
    user = models.OneToOneField(User, unique=True)


class PendingChatRoomSender(models.Model):
    pendingDicts = models.ForeignKey(PendingChatRoom, related_name="PendingChatRoom", null=True)
    senderUserName = models.CharField(max_length=40, default="", blank=True)
    readFlag = models.BooleanField(default=True)
