

import requests
import json
import re
from oauth2client import client

from amara.amara_env import amara_headers

def get_subtitles(video_url,language):
    url='https://amara.org/api/videos/'+video_url+'/languages/'+language+'/subtitles/?sub_format=srt'

    r =requests.get(url, headers=amara_headers)
    rjs= r.json()
    print(rjs['subtitles'])

def get_video_id(video_url,language_code):
    url = 'https://amara.org/api/videos/'
    urldict = dict({'video_url': video_url})
    r = requests.get(url, params=urldict, headers=amara_headers)
    json_ret = r.json()
    print(json_ret)
    if 'objects' in json_ret and len (json_ret['objects']) > 0 :
        return json_ret['objects'][0]['id']
    else:
        return post_video(video_url,language_code)

def post_video(video_url,language_code):
    url = 'https://amara.org/api/videos/'
    urldict = dict({'video_url':video_url, 'primary_audio_language_code':language_code})
    print(urldict)

    r = requests.post(url, data=urldict, headers=amara_headers )
    print(r.content)
    json_ret =  r.json()
    if 'id' in json_ret:
        return json_ret['id']
    else:
        return None

def get_actions(video_id,language_code):
    url = 'https://amara.org/api/videos/'+video_id+'/languages/'+language_code+'/subtitles/actions/'
    r = requests.get(url, headers=headers)
    print(r.json())

def post_subtitles(video_id,language_code, subtitles):
    url = 'https://amara.org/api/videos/'+video_id+'/languages/'+language_code+'/subtitles/'
    urldict = dict({'subtitles': subtitles, 'sub_format': 'srt'})
    r = requests.post(url, data=urldict, headers=amara_headers)

def convert_to_lyrics(lines):
    ret_value = ""
    rows_t = lines.split('\n')
    rows = [x for x in rows_t if len(x.strip()) > 0]
    for count,row in enumerate(rows):
        ret_value = ret_value + str(count+1) +'\r\n'
        ret_value = ret_value + '99:59:59,999 --> 99:59:59,999\r\n'
        ret_value = ret_value + row
        ret_value = ret_value + '\r\n\r\n'

    return ret_value




        #post_video(video_url='https://youtu.be/eYaDTMbxIrY',language='ru')
#get_subtitles('yYxDKmZhNPKy','ru')