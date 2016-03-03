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
from django.db.models import Q
from django.utils import timezone
import re
import json
from django.http import HttpResponse

@login_required
def mymessage(request):
    context = {}
    if request.user.is_authenticated():
        context['isLogin'] = 1
    else:
        context['isLogin'] = 0
    info = get_object_or_404(PersonInfo, user=request.user)
    context['info'] = info
    context['STATIC_URL'] = '/static/'
    context['MEDIA_URL'] = '/media/'
    return render(request, 'PatPet/person-dashboard.html', context)


# method that launch Chat
# if there is an existing charid, fetch chat history; if not, create new channel
# user2: not the one who lauch the chat (usually owner)
@login_required
def launchChat(request, usernameAccept):
    userLaucher = request.user
    userAccepter = User.objects.get(username=usernameAccept)
    chatId = ""
    if userLaucher.username <= usernameAccept:
        chatId = userLaucher.username + "+" + usernameAccept
    else:
        chatId = usernameAccept + "+" + userLaucher.username

    chatRoomExist = ChatRoom.objects.filter(chatId=chatId).count()

    if chatRoomExist == 0:
        newChatRoom = ChatRoom(chatId=chatId, currenNumUser=1)
        newChatRoom.save()
        user1, created1 = newChatRoom.chatRoom_users.get_or_create(name=request.user.username)
        user2, created2 = newChatRoom.chatRoom_users.get_or_create(name=usernameAccept)
        user1.save()
        user2.save()
        insertPendingChatRoom(userLaucher.username, usernameAccept)

        the_data = json.dumps({'chatId': chatId})
        return HttpResponse(the_data, content_type='application/json')
    else:
        oldChatRoom = ChatRoom.objects.get(chatId=chatId)
        insertPendingChatRoom(userLaucher.username, usernameAccept)
        user1, created1 = oldChatRoom.chatRoom_users.get_or_create(name=request.user.username)
        user2, created2 = oldChatRoom.chatRoom_users.get_or_create(name=usernameAccept)

        the_data = json.dumps({'chatId': chatId})
        return HttpResponse(the_data, content_type='application/json')


def insertPendingChatRoom(launchUserName, acceptUsername):
    user = User.objects.get(username=acceptUsername)
    pendingChatExist = PendingChatRoom.objects.filter(user=user).count()
    if pendingChatExist == 0:
        newPendingChat = PendingChatRoom(user=user)
        newPendingChat.save()
        pendingSentUser = oldPendingChat.PendingChatRoom.get_or_create(senderUserName=launchUserName, readFlag=False)
        pendingSentUser.save()

    else:
        oldPendingChat = PendingChatRoom.objects.get(user=user)
        pendingSentUser, created1 = oldPendingChat.PendingChatRoom.get_or_create(senderUserName=launchUserName)
        if pendingSentUser.readFlag == True:
            pendingSentUser.readFlag = False;
            pendingSentUser.save()
        pendingSentUser.save()


@login_required
def getPendingChatRoom(request):
    pendingArray = []
    oldPendingChatExist = PendingChatRoom.objects.filter(user=request.user).count()
    if oldPendingChatExist == 0:
        the_data = json.dumps(pendingArray)

        return HttpResponse(the_data, content_type='application/json')

    oldPendingChat = get_object_or_404(PendingChatRoom,user=request.user)
    allPendingChats = oldPendingChat.PendingChatRoom.all()

    for pendingChat in allPendingChats:
        if pendingChat.readFlag == False:
            pendingArray.append(pendingChat.senderUserName)
    the_data = json.dumps(pendingArray)
    return HttpResponse(the_data, content_type='application/json')


@login_required
def setPendingChatRoomUnPending(request, setUnpendingUserName):
    pendingArray = []

    oldPendingChatExist = PendingChatRoom.objects.filter(user=request.user).count()

    if oldPendingChatExist == 0:
        the_data = json.dumps(pendingArray)
        return HttpResponse(the_data, content_type='application/json')
    print ("unpending user name" + setUnpendingUserName)
    oldPendingChatRooms = PendingChatRoom.objects.get(user=request.user)
    pendingChat = oldPendingChatRooms.PendingChatRoom.get(senderUserName=setUnpendingUserName)
    pendingChat.readFlag = True
    pendingChat.save()

    pendingArray = []
    the_data = json.dumps(pendingArray)
    return HttpResponse(the_data, content_type='application/json')
    '''
        allPendingChats = oldPendingChat.PendingChatRoom.all()
        print ("here pending chatroom")
        
        
        for pendingChat in allPendingChats:
        print (pendingChat.senderUserName)
        if pendingChat.readFlag == False:
        pendingArray.append(pendingChat.senderUserName)
        the_data = json.dumps(pendingArray)
        return HttpResponse(the_data, content_type='application/json')
    '''


@login_required
def getAllRelatedChatRoom(request):
    context = {}
    allRelatedArray = []
    oldAllRelatedChatExist = PendingChatRoom.objects.filter(user=request.user).count()
    if oldAllRelatedChatExist == 0:
        allRelatedArray.append("all related data none")
        the_data = json.dumps(allRelatedArray)

        return HttpResponse(the_data, content_type='application/json')

    oldAllRelatedChat = get_object_or_404(PendingChatRoom,user=request.user)
    allRelatedChats = oldAllRelatedChat.PendingChatRoom.all()
    # print ("here all related chatroom")
    for allRelatedChat in allRelatedChats:
        allRelatedArray.append(allRelatedChat.senderUserName)
    the_data = json.dumps(allRelatedArray)
    return HttpResponse(the_data, content_type='application/json')

@login_required
def insertPendingChats(request, chatId):
    context = {}

    oldChatRoom = get_object_or_404(ChatRoom,pk=chatId)
    user3 = oldChatRoom.chatRoom_users.filter().exclude(name=request.user.username)
    receiver = user3[0]
    userGetPending = User.objects.get(username=receiver.name)

    unreadMessageRepoExist = UnreadMessages.objects.get(user=userGetPending)
    if not unreadMessageRepoExist:
        unreadMessageRepo = UnreadMessages(user=userGetPending)

    singleUnreadMsg = MessageUnread(unreadmessages=unreadMessageRepo, sendUser=request.user.person_info,
                                    messageContent="pendingChat")
    singleUnreadMsg.save()
    unreadMessageRepo, created = get_or_create(UnreadMessages, user=receiver[0])
    unreadMessageRepo.save()

    return render(request, 'PatPet/index.html', context)


@login_required
def getPendingChats(request):
    context = {}
    return render(request, 'PatPet/index.html', context)


@login_required
def getHistoryChats(request, chatId):
    oldChatRoom = get_object_or_404(ChatRoom,pk=chatId)
    historyMessages = oldChatRoom.chatRoom_messages.all()
    historyArray = []
    for message in historyMessages:
        historyArray.append([str(message), message.clickFlag])
    the_data = json.dumps(historyArray)
    return HttpResponse(the_data, content_type='application/json')

@login_required
def redirect_video(request):
    hostname = request.META['HTTP_HOST']

    hostnameArr = hostname.split(":")
    hostname = hostnameArr[0]

    port = '444'
    room = request.GET['roomid']

    print (hostname+":"+port+"/video/?roomid="+str(room))
    return redirect("https://"+hostname+":"+port+"/video/?roomid="+str(room));
