
import argparse
from pymongo import MongoClient


from legacy.blogspot_tools import iterate_blog_posts, iterate_title_and_videos, BlogPost
from tools.tool_blog_client import stripHtmlTags
import yaml


def update_blog_collection(posts_collection, blogId, apiKey, olddata=None):
    tdata = olddata if olddata else {}
    postids = set(tdata.keys())
    for post_list in iterate_blog_posts(blogId, apiKey ):
        for blogPost in iterate_title_and_videos(post_list ):

            if not blogPost:
                print("Skipping empty post")
                continue

            if not hasattr(blogPost, "postId"):
                print("Skipping post : {}".format(blogPost))
                continue
            if (blogPost.postId in postids):
                postids.remove(blogPost.postId)
            if blogPost.postId in tdata:

                update_key, update_value = {'postId': blogPost.postId}, {k: v for k, v in blogPost._asdict().items() if k not in "postId"}

                if blogPost  != tdata[blogPost.postId]:
                    print("updating {} to {}".format(update_key, update_value ))


                    posts_collection.update_one(update_key,   { '$set' : update_value } )
                    print("updated {} to {}".format(update_key, update_value))
                else:
                    print("post {} unchanged".format(blogPost.postId))
            else:
                print("inserting {} ".format(blogPost))

                posts_collection.insert_one(blogPost._asdict())
                print("inserted {} ".format(blogPost._asdict()))
    for postid in postids:
        posts_collection.delete_one({'postId': postid})
        print("post {} deleted".format(postid))

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('--blogId')
    parser.add_argument('--configFile')

    args = parser.parse_args()
    config = yaml.safe_load(open(args.configFile))
    client = MongoClient(config['mongo_connection'])
    musicblogs_database = client.musicblogs
    posts_collection= musicblogs_database['posts.'+args.blogId]


    posts_in_blog = posts_collection.find()
    posts_map = \
        { p['postId']: BlogPost(
               postId=p['postId'], title=p['title'], videoId=p['videoId'], content=p['content'], labels=p.get('labels',0), url=p.get('url', ''),
               amara_embed=p.get('amara_embed', '')
            ) for p in posts_in_blog
        }


    update_blog_collection(posts_collection, blogId=args.blogId, apiKey=config['API-KEY'], olddata=posts_map )
