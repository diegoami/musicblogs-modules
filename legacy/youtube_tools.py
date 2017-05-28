import requests
import json
import re


def verify_link(title,code,api_key):
    youtubeurl = 'https://www.googleapis.com/youtube/v3/videos?id='+code+'&key='+api_key+'&part=contentDetails'
    try:
        rytu = requests.get(youtubeurl)
        ryts= rytu.json()  
        if 'items' in ryts:
            items = ryts['items']
            if (len(items)== 0):
                return False
            else:
                if 'contentDetails' in items[0]:
                    contentDetails = items[0]['contentDetails']
                    if 'regionRestriction' in contentDetails:
                        return False
                    else:
                        return True
                else:
                    return False
                return False
        else:
            return False
    except:
        return False
    return True