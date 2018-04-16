import requests
import json
import re
from collections import namedtuple
from tools.tool_blog_client import  stripHtmlTags
BlogPost = namedtuple('BlogPost', 'postId url title videoId content labels amara_embed')



def iterate_blog_posts(id,api_key):		
    url='https://www.googleapis.com/blogger/v3/blogs/'+id+'/posts?key='+api_key
    r =requests.get(url)  
    rjs= r.json()
    yield rjs
    nextPageToken= rjs.get('nextPageToken',None)
    while (nextPageToken is not None):
        url = 'https://www.googleapis.com/blogger/v3/blogs/'+id+'/posts?pageToken='+nextPageToken+'&key='+api_key
        r = requests.get(url)
        rjs= r.json()
        yield rjs
        nextPageToken = rjs.get('nextPageToken', None)


def iterate_title_and_videos(rjs):
    if 'items' in rjs:
        items = rjs['items']
        for item in items:
            content=item['content']
            m_you_tube = re.search('src=\\\".*?youtube\.com\/embed\/([\w\-]{11})[\"\?]', content)
            m_amara_embed = re.search('amara-embed', content)
            video_id = m_you_tube.group(1) if m_you_tube else None
            yield BlogPost(postId=item['id'],
                           url=item['url'],
                           title=item['title'].strip(),
                           videoId=video_id,
                           content=stripHtmlTags(item['content']),
                           labels=item.get('labels', None),
                           amara_embed=1 if m_amara_embed else 0)

    yield None, None, None