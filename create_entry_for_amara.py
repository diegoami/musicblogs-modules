from amara.amara_env import amara_headers
import tools.tool_blog_amara

from oauth2client.tools import argparser

from tools import tool_blog_client

argparser.add_argument('--blogId')
argparser.add_argument('--postId')
argparser.add_argument('--language_code')

args = argparser.parse_args()
service, flags = tool_blog_client.login()
blogId = args.blogId
language_code = args.language_code


postId = args.postId
tools.tool_blog_amara.subtitles_workflow(blogId, postId, language_code, amara_headers)
