

import requests


def get_subtitles(video_id,language,amara_headers):
    url='https://amara.org/api/videos/'+video_id+'/languages/'+language+'/subtitles/?sub_format=srt'

    r =requests.get(url, headers=amara_headers)
    rjs= r.json()
    return rjs['subtitles']

def get_video_id(video_url,language_code,amara_headers):
    url = 'https://amara.org/api/videos/'
    urldict = dict({'video_url': video_url})
    r = requests.get(url, params=urldict, headers=amara_headers)
    json_ret = r.json()
    print(json_ret)
    if 'objects' in json_ret and len (json_ret['objects']) > 0 :
        return json_ret['objects'][0]['id']
    else:
        return post_video(video_url,language_code)


def get_video_info(video_url,amara_headers):
    url = 'https://amara.org/api/videos/'
    urldict = dict({'video_url': video_url})
    r = requests.get(url, params=urldict, headers=amara_headers)
    json_ret = r.json()
    if 'objects' in json_ret and len (json_ret['objects']) > 0 :
        return json_ret['objects'][0]


def post_video(video_url,language_code,amara_headers):
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

def get_actions(video_id,language_code,amara_headers):
    url = 'https://amara.org/api/videos/'+video_id+'/languages/'+language_code+'/subtitles/actions/'
    r = requests.get(url, headers=amara_headers)
    print(r.json())
    return r.json

def get_languages(video_id,amara_headers):
    url = 'https://amara.org/api/videos/'+video_id+'/languages/';
    r = requests.get(url, headers=amara_headers)
    rjson = r.json()
    lngs = [ o['language_code'] for o in rjson['objects']]
    return lngs

def post_subtitles(video_id,language_code, subtitles,amara_headers):
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
