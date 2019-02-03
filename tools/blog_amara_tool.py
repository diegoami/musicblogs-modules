from tools import tool_blog_client

from amaraapi import AmaraTools, AmaraVideo



class BlogAmaraTool:
    def __init__(self, amara_headers):
        self.amara_headers = amara_headers
        self.amara_tools = AmaraTools(self.amara_headers)

    def post_video_from_blog(self, blogId, postId, language_code):
        service, flags = tool_blog_client.login()
        videoId = tool_blog_client.extract_video(blogId, postId, service.posts())
        lyrics = tool_blog_client.retrieve_lyrics(service, blogId, postId)
        conv_lyrics = self.amara_tools.convert_to_lyrics(lyrics)
        amara_id = self.amara_tools.get_video_id(video_url='https://youtu.be/'+videoId, language_code=language_code)
        amara_video = AmaraVideo(self.amara_headers, amara_id)
        amara_video.get_actions(language_code)
        amara_video.post_subtitles(language_code, conv_lyrics)

    def test_add_amaratags(self, blogId, postId, language_code):
        service, flags = tool_blog_client.login()
        tool_blog_client. insert_amara_tags(blogId, postId, service.posts(), language_code)

    def subtitles_workflow(self, blogId, postId, language_code):
        self.test_add_amaratags(blogId, postId, language_code)
        self.post_video_from_blog(blogId, postId, language_code)


