from tools import tool_blog_client
import amara.amara_tools

from oauth2client.tools import argparser
from oauth2client.tools import argparser

import amara.amara_tools
from tools import tool_blog_client

#parser = argparse.ArgumentParser(description='Process some integers.', parents=[argparser])

argparser.add_argument('--blogId')
argparser.add_argument('--postId')


args = argparser.parse_args()
#youtube = tool_youtube_client.get_authenticated_service(args)
service, flags = tool_blog_client.login()
blogId=args.blogId
postId = args.postId
lyrics = tool_blog_client.retrieve_lyrics(service, blogId, postId)
conv_lyrics = amara.amara_tools.convert_to_lyrics(lyrics )
print(conv_lyrics)