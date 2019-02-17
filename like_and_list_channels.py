import argparse
import os
import traceback

from youtube3 import YoutubeClient
from googleapiclient.errors import HttpError
import operator

from blogspotapi import BlogClient, BlogPost, BlogRepository
from amara.amara_env import amara_headers

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--blogId')
    parser.add_argument('--mongo_connection', type=str, default='mongodb://localhost:27017/musicblogs')
    args = parser.parse_args()
    channelsDict = dict()
    client_secrets_file = os.path.join(os.path.dirname(__file__), 'client_secrets.json')
    youtube_client = YoutubeClient(client_secrets_file)
    blog_client = BlogClient(client_secrets_file)
    blog_repository = BlogRepository(args.mongo_connection, args.blogId, amara_headers)
    blogId = args.blogId
    for post_id, blog_post in blog_repository.posts_map.items():
        try:
            videoId = blog_post.videoId
            print('Found video ' + videoId)
            youtube_client.like_video(videoId)
            channelId = youtube_client.get_channel_id( videoId)
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

    sorted_channels = sorted(channelsDict.items(), key=operator.itemgetter(1), reverse=True)
    print(sorted_channels)
    #for channel_id, channel_name in sorted_channels:
    #    youtube_client.subscribe_channel(channel_id)