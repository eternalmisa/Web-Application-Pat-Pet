from django.conf.urls import include, url
from PatPet.views import CustomSearchView
from Team151 import settings


urlpatterns = [
     url(r'^$', 'PatPet.views.index', name='index'),
     ### Search ###
     url(r'search/$', CustomSearchView.as_view(), name='search_view'),
     url(r'search/autocomplete/', 'PatPet.views.autocomplete', name='autocomplete'),
     ### Third Party login ###
     url('', include('social.apps.django_app.urls', namespace='social')),
     url('', include('django.contrib.auth.urls', namespace='auth')),
     url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
     url(r'^login$', 'django.contrib.auth.views.login', {'template_name': 'PatPet/sign-in.html'}, name="login"),
     url(r'^logout$', 'django.contrib.auth.views.logout_then_login', name='logout'),
     ##sign_views.py
     ### Login && Register ###

     url(r'^gotosignup$', 'PatPet.sign_views.gotosignup', name="gotosignup"),
     url(r'^login/go_active$', 'PatPet.sign_views.login_active',  name="login_active"),
     url(r'^checkuser$', 'PatPet.sign_views.checkUser'),
     url(r'^checkuserForEdit$', 'PatPet.sign_views.checkUserForEdit'),
     url(r'^checkemail$', 'PatPet.sign_views.checkEmail'),
     url(r'^accounts/confirm/(?P<activation_key>\w+)/', 'PatPet.sign_views.active_account'),
     url(r'^checkemail$', 'PatPet.sign_views.checkEmail'),

     ### Pet ###
     #pet_views.py
     url(r'^pet_profile/(?P<pid>\d+)$', 'PatPet.pet_views.pet_profile', name='pet_profile'),
     url(r'^add_pet$', 'PatPet.pet_views.add_pet', name='add_pet'),
     url(r'^delete_pet/(?P<pid>\d+)$', 'PatPet.pet_views.delete_pet', name='delete_pet'),
     url(r'^delete_photo/(?P<index>\d+)/(?P<pid>\d+)$', 'PatPet.pet_views.delete_photo', name='delete_photo'),
     url(r'^delete_video/(?P<index>\d+)/(?P<vid>\d+)$', 'PatPet.pet_views.delete_video', name='delete_video'),


     ### Person ###
     #person_views.py
     url(r'^myprofile$', 'PatPet.person_views.myprofile', name='myprofile'),
     url(r'^person_profile/(?P<uid>\d+)$', 'PatPet.person_views.person_profile', name='person_profile'),
     url(r'^edit_profile/$', 'PatPet.person_views.edit_profile', name='edit_profile'),

     ### Transaction ###
     #transaction_views.py
     url(r'^transaction_renter/(?P<tid>\d+)$', 'PatPet.transaction_views.transaction_renter', name='transaction_renter'),
     url(r'^transaction_owner/(?P<tid>\d+)$', 'PatPet.transaction_views.transaction_owner', name='transaction_owner'),
     url(r'^transaction_visitor/(?P<tid>\d+)$', 'PatPet.transaction_views.transaction_visitor', name='transaction_visitor'),
     url(r'^transaction_renter/(?P<tid>\d+)$', 'PatPet.transaction_views.transaction_renter', name='transaction_renter'),
     url(r'^transaction/(?P<tid>\d+)$', 'PatPet.transaction_views.transaction', name='transaction'),
     url(r'^owner_submit_review/(?P<tid>\d+)$', 'PatPet.transaction_views.owner_submit_review', name='owner_submit_review'),
     url(r'^renter_submit_review/(?P<tid>\d+)$', 'PatPet.transaction_views.renter_submit_review', name='renter_submit_review'),
     url(r'^owner_submit_review/(?P<tid>\d+)$', 'PatPet.transaction_views.owner_submit_review', name='owner_submit_review'),
     url(r'^upload_transaction_images/(?P<tid>\d+)$', 'PatPet.transaction_views.upload_transaction_images',
         name='upload_transaction_images'),
     url(r'^add_transaction/(?P<pid>\d+)$', 'PatPet.transaction_views.add_transaction', name='add_transaction'),
     url(r'^upload_transaction_videos/(?P<tid>\d+)$', 'PatPet.transaction_views.upload_transaction_videos',
         name='upload_transaction_videos'),
     url(r'^upload_moment_content/(?P<tid>\d+)$', 'PatPet.transaction_views.upload_moment_content', name='upload_moment_content'),
     url(r'^getmoments/(?P<tid>\d+)$','PatPet.transaction_views.getmoments',name='getmoments'),
     url(r'^delete_moment/(?P<cid>\d+)$','PatPet.transaction_views.delete_moment',name='delete_moment'),



     ### Chat ####
     #chat_views.py
     url(r'^launchChat/(?P<usernameAccept>.*)$', 'PatPet.chat_views.launchChat', name='launchChat'),
     url(r'^getHistoryChats/(?P<chatId>.*)$', 'PatPet.chat_views.getHistoryChats', name='getHistoryChat'),
     url(r'^setPendingChatRoomUnPending/(?P<setUnpendingUserName>.*)$', 'PatPet.chat_views.setPendingChatRoomUnPending',
         name='setPendingChatRoomUnPending'),
     url(r'^getPendingChatRoom', 'PatPet.chat_views.getPendingChatRoom', name='getPendingChatRoom'),
     url(r'^getAllRelatedChatRoom', 'PatPet.chat_views.getAllRelatedChatRoom', name='getAllRelatedChatRoom'),
     url(r'^mymessage$', 'PatPet.chat_views.mymessage', name='mymessage'),
     url(r'^video/$','PatPet.chat_views.redirect_video',name='redirect_video'),

]
