import requests
import json
import re


def iterate_blog_posts(id,api_key):		
    url='https://www.googleapis.com/blogger/v3/blogs/'+id+'/posts?key='+api_key
    r =requests.get(url)  
    rjs= r.json()
    yield rjs
    nextPageToken= rjs['nextPageToken']
    while (nextPageToken is not None):
        url = 'https://www.googleapis.com/blogger/v3/blogs/'+id+'/posts?pageToken='+nextPageToken+'&key='+api_key
        r = requests.get(url)
        rjs= r.json()
        yield rjs
        if 'nextPageToken' in rjs:
            nextPageToken= rjs['nextPageToken']
        else:
            nextPageToken= None
            break

def retrieve_title_and_videos(rjs,api_key):
    if 'items' in rjs:
        items = rjs['items']
        for item in items:
            content=item['content']
            m = re.search('src=\\\".*?youtube\.com\/embed\/(.*?)[\"\?]', content)
            if m:
                return item['title'],m.group(1)
    else:
        return None, None