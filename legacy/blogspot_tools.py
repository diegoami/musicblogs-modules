import requests
import json
import re
from collections import namedtuple
from tools.tool_blog_client import  stripHtmlTags
BlogPost = namedtuple('BlogPost', 'postId title videoId content labels')



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
            m = re.search('src=\\\".*?youtube\.com\/embed\/([\w\-]{11})[\"\?]', content)
            if m:
                yield BlogPost(postId =item['id'], title=item['title'], videoId=m.group(1), content=stripHtmlTags(item['content']), labels=item.get('labels', None))
            else:
                yield BlogPost(postId=item['id'], title=item['title'], videoId=None, content=stripHtmlTags(item['content']), labels=item['labels'])
    else:
        yield None, None, None