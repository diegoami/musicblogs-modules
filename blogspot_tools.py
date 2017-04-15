import requests
import json


def iterate_blog_posts(id,api_key):		
	url='https://www.googleapis.com/blogger/v3/blogs/'+id+'/posts?key='+api_key
	r =requests.get(url)
	rjs= r.json()
	yield rjs
	nextPageToken= rjs['nextPageToken']
	while (nextPageToken is not None):
		url = 'https://www.googleapis.com/blogger/v3/blogs/'+id+'/posts?pageToken='+nextPageToken+'&key='+api_key
		r = requests.get(url)
		rjs= r.json()
		yield rjs
		if 'nextPageToken' in rjs:
		    nextPageToken= rjs['nextPageToken']
		else:
		    nextPageToken= None
		    break