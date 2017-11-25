from tools import tool_blog_client

import amara.amara_tools




def post_video_from_blog(blogId, postId, language_code):
    service, flags = tool_blog_client.login()
    videoId = tool_blog_client.extract_video(blogId, postId, service.posts())
    lyrics = tool_blog_client.retrieve_lyrics(service, blogId, postId)
    conv_lyrics = amara.amara_tools.convert_to_lyrics(lyrics )
    videoId = amara.amara_tools.get_video_id(video_url='https://youtu.be/'+videoId,language_code=language_code)
    amara.amara_tools.get_actions(videoId ,language_code)
    amara.amara_tools.post_subtitles(videoId, language_code, conv_lyrics )

def test_add_amaratags( blogId, postId, language_code):
    service, flags = tool_blog_client.login()
    tool_blog_client. insert_amara_tags(blogId, postId, service.posts(), language_code)

def subtitles_workflow(blogId, postId, language_code):
    test_add_amaratags(blogId, postId, language_code)
    post_video_from_blog(blogId, postId, language_code)

