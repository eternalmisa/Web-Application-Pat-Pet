from django.shortcuts import get_object_or_404
from django.utils.html import strip_tags
from django_socketio import events
from datetime import datetime
import datetime
from models import * 
import json
# from views import add_transaction as add_transaction

@events.on_message(channel="^")
def message(request, socket, context, message):
    """
    Event handler for a room receiving a message. First validates a
    joining user's name and sends them the list of users.
    """

    # room = get_object_or_404(ChatRoom, id=message["room"])
    room = get_object_or_404(ChatRoom,chatId=message['room'])
    


    '''
    try:
        user = context["user"]
    except KeyError:
        return
    '''
    username = message["user"]
    user = User.objects.get(username=username)

    if message["action"] == "message":
        message["message"] = strip_tags(message["message"])        
        if not message["message"]:
            return 

        # message_chat = MessageChat(messageDicts=room,sendUser=user.person_info,messageContent=message["message"],messageType="ChatMessage")
        message_chat = MessageChat(messageDicts=room,sendUser=user.person_info,messageContent=json.dumps(message),messageType="ChatMessage",petId=0,clickFlag=False)
        message_chat.save()

    elif message["action"] == "invitation":
        # message_invitation = MessageChat(messageDicts=room,sendUser=user.person_info,messageContent=message["message"],messageType="Invitation")
        message_invitation = MessageChat(messageDicts=room,sendUser=user.person_info,messageContent=json.dumps(message),messageType="Invitation",petId=message["petid"],clickFlag=False)
        message_invitation.save()

    elif message["action"] == "accept":

        chatIdArr = message['room'].split("+")
        if chatIdArr[0] == username:
            anotherUserName = chatIdArr[1]
        else:
            anotherUserName = chatIdArr[0]
        anotherUser = User.objects.get(username=anotherUserName)
        message_accept = MessageChat(messageDicts=room,sendUser=user.person_info,messageContent=json.dumps(message),messageType="Accept",petId=0,clickFlag=False)
        

        message_acceptExist = MessageChat.objects.filter(messageDicts=room,sendUser=anotherUser.person_info,messageType="Invitation",petId=message["petid"],clickFlag=False).count()
        if  message_acceptExist != 0:
            message_unset_invitations = MessageChat.objects.filter(messageDicts=room,sendUser=anotherUser.person_info,messageType="Invitation",petId=message["petid"],clickFlag=False)
            for message_unset_invitation in message_unset_invitations:
                message_unset_invitation.clickFlag = True
                message_unset_invitation.save()
        
        pid = message["petid"]
        new_pet = PetInfo.objects.get(id=pid)
        new_pet.save()
        renter=anotherUser
        owner= new_pet.owner
        new_owner = PersonInfo.objects.get(user=owner)
        new_renter = PersonInfo.objects.get(user=renter)


        startTimeString = message["start"]
        endTimeString = message["end"]

        parsedStart = datetime.datetime.strptime(startTimeString,'%m/%d/%Y')
        parsedEnd = datetime.datetime.strptime(endTimeString,'%m/%d/%Y')

        new_status = Status(statusText="Status: Started",price=1.00,starttime=parsedStart,endtime=parsedEnd)
        new_status.save()
        new_moment = Moment()
        new_moment.save()
        new_activity = Activity(owner=new_owner,renter=new_renter,pet=new_pet,status=new_status,moment=new_moment)
        new_activity.save()
        message["url"] = ("/transaction_owner/"+str(new_activity.id))

        message_accept.save()

    elif message["action"] == "reject":

        chatIdArr = message['room'].split("+")
        if chatIdArr[0] == username:
            anotherUserName = chatIdArr[1]
        else:
            anotherUserName = chatIdArr[0]
        anotherUser = User.objects.get(username=anotherUserName)
        # message_reject = MessageChat(messageDicts=room,sendUser=user.person_info,messageContent=message["message"],messageType="Reject")
        message_reject = MessageChat(messageDicts=room,sendUser=user.person_info,messageContent=json.dumps(message),messageType="Reject",petId=0,clickFlag=False)
        message_reject.save()
        
        # print("pet id: " + str(message["petid"]))
        # print("user name: " + str(user.username))
        # print("Oter user name: " + str(anotherUserName))
        # print("Oter user name type: " + str(type(anotherUserName)))
        # print("Chat id: " + str(message["room"]))

        message_acceptExist = MessageChat.objects.filter(messageDicts=room,sendUser=anotherUser.person_info,messageType="Invitation",petId=message["petid"],clickFlag=False).count()
        if  message_acceptExist != 0:
            # print("Inside~~~~~~~~~")
            message_unset_invitations = MessageChat.objects.filter(messageDicts=room,sendUser=anotherUser.person_info,messageType="Invitation",petId=message["petid"],clickFlag=False)
            for message_unset_invitation in message_unset_invitations:
                message_unset_invitation.clickFlag = True
                message_unset_invitation.save()

    elif message["action"] == "videorequest":
        message_video_request = MessageChat(messageDicts=room,sendUser=user.person_info,messageContent=json.dumps(message),messageType="VideoRequest",petId=0,clickFlag=False)
        message_video_request.save()
        print ("video request " + message['user'] + message['user2'])

    elif message["action"] == "acceptvideo":
        print ("accpet video" + message['user'] + message['user2'])
        chatIdArr = message['room'].split("+")
        if chatIdArr[0] == username:
            anotherUserName = chatIdArr[1]
        else:
            anotherUserName = chatIdArr[0]
        anotherUser = User.objects.get(username=anotherUserName)
        message_accept = MessageChat(messageDicts=room,sendUser=user.person_info,messageContent=json.dumps(message),messageType="AcceptVideoChat",petId=0,clickFlag=False)
        

        message_acceptExist = MessageChat.objects.filter(messageDicts=room,sendUser=anotherUser.person_info,messageType="VideoRequest",petId=0,clickFlag=False).count()
        if  message_acceptExist != 0:
            message_unset_video_requests = MessageChat.objects.filter(messageDicts=room,sendUser=anotherUser.person_info,messageType="VideoRequest",petId=0,clickFlag=False)
            for message_unset_video_request in message_unset_video_requests:
                message_unset_video_request.clickFlag = True
                message_unset_video_request.save()
        
        message["url"] = ("/video_chat/"+str(message['room']))

        message_accept.save()

    elif message["action"] == "rejectvideo":
        print ("reject video " + message['user'] + message['user2'])
        chatIdArr = message['room'].split("+")
        if chatIdArr[0] == username:
            anotherUserName = chatIdArr[1]
        else:
            anotherUserName = chatIdArr[0]
        anotherUser = User.objects.get(username=anotherUserName)
        message_reject = MessageChat(messageDicts=room,sendUser=user.person_info,messageContent=json.dumps(message),messageType="RejectVideoChat",petId=0,clickFlag=False)
        message_reject.save()
        
        message_acceptExist = MessageChat.objects.filter(messageDicts=room,sendUser=anotherUser.person_info,messageType="VideoRequest",petId=0,clickFlag=False).count()
        if  message_acceptExist != 0:
            message_unset_video_requests = MessageChat.objects.filter(messageDicts=room,sendUser=anotherUser.person_info,messageType="VideoRequest",petId=0,clickFlag=False)
            for message_unset_video_request in message_unset_video_requests:
                message_unset_video_request.clickFlag = True
                message_unset_video_request.save()

    message["name"] = user.username
    socket.send_and_broadcast_channel(message)


@events.on_finish(channel="^room-")
def finish(request, socket, context):
    """
    Event handler for a socket session ending in a room. Broadcast
    the user leaving and delete them from the DB.
    """
    try:
        user = context["user"]
    except KeyError:
        return
    left = {"action": "leave", "name": user.name, "id": user.id}
    socket.broadcast_channel(left)
    # user.delete()
