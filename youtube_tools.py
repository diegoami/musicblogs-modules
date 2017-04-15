import requests
import json
import re


def verify_link(title,code,api_key):
    youtubeurl = 'https://www.googleapis.com/youtube/v3/videos?id='+code+'&key='+api_key+'&part=status'
    try:
        rytu = requests.get(youtubeurl)
        ryts= rytu.json()  
        if 'items' in ryts:
            items = ryts['items']
            if (len(items)== 0):
                return False
        else:
            return False
    except:
        return False
    return True