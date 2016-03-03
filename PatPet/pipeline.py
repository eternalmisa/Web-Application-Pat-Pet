from social.pipeline.partial import partial
from PatPet.models import *


@partial
def get_profile_picture(strategy, user, response, details, is_new=False, *args, **kwargs):
    if "facebook" in kwargs['backend'].redirect_uri:
        url = 'http://graph.facebook.com/{0}/picture'.format(response['id'])
    elif "twitter" in kwargs['backend'].redirect_uri:
        if response['profile_image_url'] != '':
            url = response['profile_image_url']
    elif "google" in kwargs['backend'].redirect_uri:
        if response['image'].get('url') is not None:
            url = response['image'].get('url')
    print url

    if PersonInfo.objects.filter(user=user).count() == 0:
        info = PersonInfo.objects.create(user=user, person_avatar=url, is_third="1")
        info.save()
