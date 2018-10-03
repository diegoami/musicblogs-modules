import tools.tool_blog_amara
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

tools.tool_blog_amara.subtitles_workflow(blogId, postId, language_code, amara_headers)
