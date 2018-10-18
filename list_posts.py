
import argparse
from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()



from legacy.blogspot_tools import iterate_blog_posts, iterate_title_and_videos, BlogPost
import yaml


def update_blog_collection(posts_collection, blogId, apiKey, olddata=None):
    tdata = olddata if olddata else {}
    postids = set(tdata.keys())
    for post_list in iterate_blog_posts(blogId, apiKey ):
        for blogPost in iterate_title_and_videos(post_list ):

            if not blogPost:
                continue

            if not hasattr(blogPost, "postId"):
                continue
            if (blogPost.postId in postids):
                postids.remove(blogPost.postId)
            if blogPost.postId in tdata:

                update_key, update_value = {'postId': blogPost.postId}, {k: v for k, v in blogPost._asdict().items() if k not in "postId"}

                if blogPost  != tdata[blogPost.postId]:
                    print("updating {}".format(update_key ))


                    posts_collection.update_one(update_key,   { '$set' : update_value } )
                    print("updated {} ".format(update_key))
                else:
                    print("post {} unchanged".format(blogPost.postId))
            else:
                print("inserting {} ".format(blogPost.postId))
                posts_collection.insert_one(blogPost._asdict())
                print("inserted {} ".format(blogPost.postId))
    for postid in postids:
        posts_collection.delete_one({'postId': postid})
        print("post {} deleted".format(postid))


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('--blogId')
    parser.add_argument('--configFile')
    api_key = os.getenv("BLOG-API-KEY")
    mongo_connection = os.getenv("mongo_connection")

    args = parser.parse_args()
    if (args.configFile):
        config = yaml.safe_load(open(args.configFile))
        blog_api_key = config['API-KEY']
        mongo_connection = config['mongo_connection']
    client = MongoClient(mongo_connection)
    musicblogs_database = client.musicblogs
    posts_collection= musicblogs_database['posts.'+args.blogId]


    posts_in_blog = posts_collection.find()
    posts_map = \
        { p['postId']: BlogPost(
               postId=p['postId'], title=p['title'], videoId=p['videoId'], content=p['content'], labels=p.get('labels',0), url=p.get('url', ''),
               amara_embed=p.get('amara_embed', '')
            ) for p in posts_in_blog
        }


    update_blog_collection(posts_collection, blogId=args.blogId, apiKey=api_key, olddata=posts_map )
