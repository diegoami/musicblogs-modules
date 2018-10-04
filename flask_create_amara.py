from flask import Flask
from flask_restful import Resource, Api
from flask import request
import tools.tool_blog_amara
app = Flask(__name__)
api = Api(app)

from flask_restful import reqparse, abort, Api, Resource
import os

from flask_cors import CORS

from dotenv import load_dotenv
load_dotenv()

amara_headers={
    "X-api-username": os.getenv('AMARA-X-api-username'),
    "X-api-key": os.getenv('AMARA-X-api-key')
}

parser = reqparse.RequestParser()
parser.add_argument('blogId')
parser.add_argument('postId')
parser.add_argument('language_code')



class CreateAmara(Resource):
    def get(self, blogId, postId, language_code):
        print(blogId)
        print(postId)
        print(language_code)
        tools.tool_blog_amara.subtitles_workflow(blogId, postId, language_code, amara_headers)
        return {'ok' : 1, 'blogId' : blogId, 'postId' : postId, 'language_code' : language_code}

api.add_resource(CreateAmara, '/bae/<blogId>/<postId>/<language_code>')

if __name__ == '__main__':
    CORS(app)
    app.run(port=5001, threaded=True, host=('0.0.0.0'))
