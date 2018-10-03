
import argparse
import traceback
from pymongo import MongoClient
from amara.amara_tools import get_subtitles, get_languages, get_video_info
from amara.amara_env import amara_headers

from legacy.blogspot_tools import iterate_blog_posts, iterate_title_and_videos
import yaml


def update_subtitles_collection(subtitles_collection, blogId, languages_str, apiKey):
    languages = languages_str.split(',')
    for post_list in iterate_blog_posts(blogId, apiKey ):
        for blogPost in iterate_title_and_videos(post_list ):
            if hasattr(blogPost, "labels"):
                labels = blogPost.labels
                video_url = blogPost.videoId

                if labels and ('subtitled' in labels or 'SUBTITLED' in labels):
                    print("Trying to get video for {}".format(video_url))
                    try:
                        video_info = get_video_info('https://youtu.be/'+video_url, amara_headers)
                        if (video_info):
                            print(video_info)
                            video_id = video_info["id"]
                            if (video_id):
                                languages_video = get_languages(video_id, amara_headers)

                                common_languages = [l for l in languages_video if l in languages]
                                if (common_languages):
                                    sel_lang = common_languages[0]
                                    subtitles = get_subtitles(video_id, sel_lang, amara_headers)
                                    if (subtitles and len(subtitles) > 0):
                                        print("Saving subtitles for {}".format(video_id))
                                        subtitles_collection.replace_one(
                                            filter={"video_url": video_url},
                                            replacement={"video_url" : video_url, "video_id" : video_id, "lang" : sel_lang, "subtitles" : subtitles},
                                            upsert = True
                                        );

                    except:
                        print("Could not process {} from {}".format(video_id, blogPost.url))
                        traceback.print_exc()

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('--blogId')
    parser.add_argument('--configFile')
    parser.add_argument('--languages')

    args = parser.parse_args()
    api_key = os.getenv("API-KEY")
    mongo_connection = os.getenv("mongo_connection")

    args = parser.parse_args()
    if (args.configFile):
        config = yaml.safe_load(open(args.configFile))
        blog_api_key = config['API-KEY']
        mongo_connection = config['mongo_connection']


    client = MongoClient(mongo_connection)
    musicblogs_database = client.musicblogs
    subtitles_collection= musicblogs_database['subtitles.'+args.blogId]
    musicblogs_database = client.musicblogs
    update_subtitles_collection(subtitles_collection=subtitles_collection, blogId=args.blogId, languages_str=args.languages, apiKey=api_key)