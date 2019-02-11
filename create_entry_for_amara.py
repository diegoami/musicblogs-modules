from tools.blog_amara_tool import BlogAmaraTool
from amara.amara_env import amara_headers
from oauth2client.tools import argparser

from tools.blog_amara_tool import BlogAmaraTool

argparser.add_argument('--blogId')
argparser.add_argument('--postId')
argparser.add_argument('--language_code')

args = argparser.parse_args()
blogId = args.blogId
language_code = args.language_code
postId = args.postId

blog_amara_tool = BlogAmaraTool(amara_headers)
blog_amara_tool.subtitles_workflow(blogId, postId, language_code)
