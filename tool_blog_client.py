import sys
from googleapiclient import sample_tools
import re

from apiclient.errors import HttpError

def login():
    service, flags = sample_tools.init(
        sys.argv, 'blogger', 'v3', __doc__, __file__,
        scope='https://www.googleapis.com/auth/blogger')
    return service, flags

def replace_object_in_blog_post(blogId, postId):
    service, flags = login()
    posts = service.posts()
    request = posts.get(blogId=blogId,postId=postId)
    posts_doc = request.execute()
    content =  posts_doc['content']
    print('Processing post '+postId+':'+posts_doc['title'])
    my = re.search('youtube\.com\/v\/([\w\-]{11})', content)
    obind1 = content.find('<object')
    obind2 = content.find('object>')

    if my and obind1 >= 0 and obind2 >=0 :
        newcontent = content[0:obind1]+'<iframe src="https://www.youtube.com/embed/'+my.group(1)+'" width="640" height="390" frameborder="0" allowfullscreen></iframe>'+content[obind2+7:len(content)]
        posts_doc['content'] = newcontent
        request = posts.update(blogId=blogId,postId=postId,body=posts_doc)
        print('Replacing object' + postId)
        request.execute()


def update_video_in_blog_post(blogId, postId, old_youtube_ref,new_youtube_ref):
    service, flags = login()
    posts = service.posts()
    request = posts.get(blogId=blogId,postId=postId)
    posts_doc = request.execute()
    posts_doc['content'] = posts_doc['content'].replace(old_youtube_ref,new_youtube_ref)
    request = posts.update(blogId=blogId,postId=postId,body=posts_doc)
    print(request)
    request.execute()


def iterate_blog_posts(blogId):
    service, flags = login()
    posts = service.posts()
    request = posts.list(blogId=blogId)
    while request != None:
        posts_doc = request.execute()
        if 'items' in posts_doc and not (posts_doc['items'] is None):
            for post in posts_doc['items']:
                yield post
        request = posts.list_next(request, posts_doc)

blog_id= '446998987295244185'
for post in iterate_blog_posts(blog_id):
    try:
        replace_object_in_blog_post(blog_id, post['id'])
    except HttpError as e:
        print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))