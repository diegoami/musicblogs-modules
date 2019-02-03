from tools.blog_amara_tool import BlogAmaraTool
import os
from oauth2client.tools import argparser

from tools import tool_blog_client
from dotenv import load_dotenv
load_dotenv()


argparser.add_argument('--blogId')
argparser.add_argument('--postId')
argparser.add_argument('--language_code')

args = argparser.parse_args()
service, flags = tool_blog_client.login()
blogId = args.blogId
language_code = args.language_code


postId = args.postId
amara_headers={
    "X-api-username": os.getenv('AMARA-X-api-username'),
    "X-api-key": os.getenv('AMARA-X-api-key')
}

blog_amara_tool = BlogAmaraTool(amara_headers)
blog_amara_tool.subtitles_workflow(blogId, postId, language_code)
