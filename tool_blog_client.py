import sys
from googleapiclient import sample_tools

def login():
    service, flags = sample_tools.init(
        sys.argv, 'blogger', 'v3', __doc__, __file__,
        scope='https://www.googleapis.com/auth/blogger')
    return service, flags

def update_video_in_blog_post(blogId, postId, old_youtube_ref,new_youtube_ref):
    service, flags = login()
    posts = service.posts()
    request = posts.get(blogId=blogId,postId=postId)
    posts_doc = request.execute()
    posts_doc['content'] = posts_doc['content'].replace(old_youtube_ref,new_youtube_ref)
    request = posts.update(blogId=blogId,postId=postId,body=posts_doc)
    print(request)
    request.execute()

