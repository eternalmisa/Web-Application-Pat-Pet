import urllib2
import json
from django import forms
#import Error


'''
Input: street, city, state
output: [latitude, longitude]
Description:
    Given input address, return a geo position.
'''
def format_address_helper(street, city, state):
    street = street.strip()
    street = street.replace(" ", "%20")
    city = city.strip()
    city = city.replace(" ", "%20")
    state = state.strip()
    state = state.replace(" ", "%20")
    space = "%20"
    addr = street + space + city + space + state
    google_map_url = "http://maps.googleapis.com/maps/api/geocode/json?address="+addr+"key=AIzaSyAIzGgFgc7Ciut7Jt3muaPaI3VL8Z67kTE"
    try:
        content = urllib2.urlopen(google_map_url).read()
    except Exception as e:
        raise Exception("Bad url format!")

    try:
        content_json = json.loads(content) 
    except Exception as e:
        raise Exception("Bad returned value format!")
    
    try:
        if content_json['status'] == 'OK' and len(content_json['results']) >= 1:
            print content_json['results'][0]['formatted_address']
            lat = content_json['results'][0]['geometry']['location']['lat']
            lng = content_json['results'][0]['geometry']['location']['lng']
            return [lat, lng]
        else:
            raise Exception("Can't find location!")
    except Exception:
        raise Exception("Bad return format!")


if __name__ =='__main__':
    street = raw_input("Input street addr")
    city = raw_input("Input city addr")
    state = raw_input("Input state addr")
    print(format_address_helper(street, city, state))
