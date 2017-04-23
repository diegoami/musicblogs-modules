

import traceback

import tool_youtube_client
from apiclient.errors import HttpError
from oauth2client.tools import argparser

from tools import tool_blog_client

if __name__ == "__main__":
    argparser.add_argument('--blogId')
    args = argparser.parse_args()
    channelsDict = dict()
    youtube = tool_youtube_client.get_authenticated_service(args)
    service, flags = tool_blog_client.login()
    blogId=args.blogId
    for post in tool_blog_client.iterate_blog_posts(service, blogId):
        try:
            videoId = tool_blog_client.extract_video(blogId, post['id'], service.posts())
            print('Found video ' + videoId)
            tool_youtube_client.like_video(youtube, videoId)
            channelId = tool_youtube_client.get_channel_id(youtube, videoId)
            print('Found channel ' + channelId)
            if not channelId in channelsDict:
                channelsDict[channelId] = 0
            channelsDict[channelId] = channelsDict[channelId]+1
            print('Found channel ' + channelId + ':'+str(channelsDict[channelId]))
        except HttpError as e:
            print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
        except Exception as e:
            traceback.print_exc()
        else:
            print('Liked video ' + videoId)

    sorted_channels = sorted(channelsDict.items(), key=lambda x: x[1], reverse=True)
    print(sorted_channels)
    for k,v in sorted_channels:
        tool_youtube_client.subscribe_channel(youtube, k)