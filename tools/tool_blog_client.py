import sys
from googleapiclient import sample_tools
import re
from bs4 import BeautifulSoup  # Or from BeautifulSoup import BeautifulSoup
import datetime

from oauth2client.tools import argparser, run_flow

import argparse
import os

from googleapiclient import discovery
from googleapiclient.http import build_http
from oauth2client import client
from oauth2client import file
from oauth2client import tools



def stripHtmlTags(htmlTxt):
    if htmlTxt is None:
        return None
    else:
        all_lines = BeautifulSoup(htmlTxt).findAll(text=True)
        not_empty_lines = [line for line in all_lines if len(line) > 0]
        return '\n'.join(not_empty_lines)

from apiclient.errors import HttpError

def login():
    service, flags = sample_tools.init(
        sys.argv+['--noauth_local_webserver'], 'blogger', 'v3', __doc__, __file__,
        scope='https://www.googleapis.com/auth/blogger')
    return service, flags

def init_alt(argv, name, version, doc, filename, scope=None, parents=[], discovery_filename=None):
    if scope is None:
        scope = 'https://www.googleapis.com/auth/' + name

    # Parser command-line arguments.
    parent_parsers = [tools.argparser]
    parent_parsers.extend(parents)
    parser = argparse.ArgumentParser(
        description=doc,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=parent_parsers)
    flags = parser.parse_args(argv[1:])

    # Name of a file containing the OAuth 2.0 information for this
    # application, including client_id and client_secret, which are found
    # on the API Access tab on the Google APIs
    # Console <http://code.google.com/apis/console>.
    client_secrets = os.path.join(os.path.dirname(filename),
                                  'client_secrets.json')

    # Set up a Flow object to be used if we need to authenticate.
    flow = client.flow_from_clientsecrets(client_secrets,
                                          scope=scope,
                                          message=tools.message_if_missing(client_secrets))

    # Prepare credentials, and authorize HTTP object with them.
    # If the credentials don't exist or are invalid run through the native client
    # flow. The Storage object will ensure that if successful the good
    # credentials will get written back to a file.
    storage = file.Storage(name + '.dat')
    credentials = storage.get()
    if credentials is None or credentials.invalid:
        flags.noauth_local_webserver = True
        credentials = tools.run_flow(flow, storage, flags)
    http = credentials.authorize(http=build_http())
    if discovery_filename is None:
        # Construct a service object via the discovery service.
        service = discovery.build(name, version, http=http)
    else:
        # Construct a service object using a local discovery document file.
        with open(discovery_filename) as discovery_file:
            service = discovery.build_from_document(
                discovery_file.read(),
                base='https://www.googleapis.com/',
                http=http)
    return (service, flags)


def replace_object_in_blog_post(service, blogId, postId):
    posts = service.posts()
    content, videoId, posts_doc = extract_content_and_video(blogId, postId, posts)
    obind1 = content.find('<object')
    obind2 = content.find('object>')

    if videoId and obind1 >= 0 and obind2 >=0 :
        newcontent = content[0:obind1]+'<iframe src="https://www.youtube.com/embed/'+videoId+'" width="640" height="390" frameborder="0" allowfullscreen></iframe>'+content[obind2+7:len(content)]
        posts_doc['content'] = newcontent
        request = posts.update(blogId=blogId,postId=postId,body=posts_doc)
        print('Replacing object' + postId)
        request.execute()

def extract_video(blogId, postId, posts):
    return extract_content_and_video(blogId, postId, posts)['videoId']

def extract_content_and_video(blogId, postId, posts):
    request = posts.get(blogId=blogId, postId=postId)
    posts_doc = request.execute()
    content = posts_doc['content']
    #print('Processing post ' + postId + ':' + posts_doc['title'])
    #search_youtube = re.search('youtube\.com\/v\/([\w\-]{11})', content)
    search_youtube = re.search('\\\".*?youtube\.com\/embed\/([\w\-]{11})[\"\?]', content)
    videoId = None
    if search_youtube :
        videoId = search_youtube.group(1)
    result_dict = {'content':content, 'videoId': videoId, 'posts_doc': posts_doc}
    return result_dict

def insert_amara_tags(blogId, postId, posts, language_code):
    result_dict = extract_content_and_video(blogId, postId, posts)
    content, videoId, posts_doc = result_dict['content'],result_dict['videoId'],result_dict['posts_doc']
    if content.find('amara') > -1:
        return
    pos_iframe= content.find('<iframe')
    snippet_amara = '<div class="amara-embed" data-height="390px" data-resizable="true" data-show-subtitles-default="true" data-url="http://www.youtube.com/watch?v='+videoId+'" data-width="640px" data-initial-language="'+language_code+'"></div></br>'
    newContent = content[0:pos_iframe]+snippet_amara +content[pos_iframe:len(content)]
    posts_doc['content'] = newContent
    posts_doc['labels'].append('subtitled')
    posts_doc['updated'] = posts_doc['published'] = str(datetime.datetime.now().isoformat(timespec='microseconds'))
    request = posts.update(blogId=blogId,postId=postId,body=posts_doc)
    request.execute()


def update_video_in_blog_post(blogId, postId, old_youtube_ref,new_youtube_ref, posts):
    request = posts.get(blogId=blogId,postId=postId)
    posts_doc = request.execute()
    posts_doc['content'] = posts_doc['content'].replace(old_youtube_ref,new_youtube_ref)
    request = posts.update(blogId=blogId,postId=postId,body=posts_doc)
    request.execute()

def retrieve_lyrics(service, blogId, postId ):
    request = service.posts().get(blogId=blogId, postId=postId)
    posts_doc = request.execute()
    content = posts_doc['content']
    return stripHtmlTags(content )


def iterate_blog_posts(service, blogId):

    posts = service.posts()
    request = posts.list(blogId=blogId)
    while request != None:
        posts_doc = request.execute()
        if 'items' in posts_doc and not (posts_doc['items'] is None):
            for post in posts_doc['items']:
                yield post
        request = posts.list_next(request, posts_doc)

def test_drive():
    blogId= '446998987295244185'
    service, flags = login()
    for post in iterate_blog_posts(service, blogId):
        try:
            replace_object_in_blog_post(service, blogId, post['id'])
        except HttpError as e:
            print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
