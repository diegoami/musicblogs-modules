from amaraapi import AmaraTools, AmaraVideo
from blogspotapi import BlogClient


class BlogAmaraTool:
    def __init__(self, amara_headers, config_file):
        self.amara_headers = amara_headers
        self.amara_tools = AmaraTools(self.amara_headers)
        self.blog_client = BlogClient(config_file)

    def post_video_from_blog(self, blogId, postId, language_code):
        videoId = self.blog_client.extract_video(blogId, postId)
        lyrics = self.blog_client.retrieve_lyrics(blogId, postId)
        conv_lyrics = self.amara_tools.convert_to_lyrics(lyrics)
        amara_id = self.amara_tools.get_video_id(video_url='https://youtu.be/'+videoId, language_code=language_code)
        amara_video = AmaraVideo(self.amara_headers, amara_id)
        amara_video.get_actions(language_code)
        amara_video.post_subtitles(language_code, conv_lyrics)


    def subtitles_workflow(self, blogId, postId, language_code):
        self.blog_client.insert_amara_tags(blogId, postId, language_code)
        self.post_video_from_blog(blogId, postId, language_code)


