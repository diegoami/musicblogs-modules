import csv
import sys

import youtube_tools

import blogspot_tools
import parser
import pickle
import datetime
import time
import environment as env
import smtplib
from email.mime.text import MIMEText
import argparse


def sendmail_video(subject,text):
    print("Now sending mail....")
    print(subject)
    print(text)
    """
    msg = MIMEText(text)
    msg['Subject'] = subject
    msg['From'] = env.DESTINATION_MAIL
    msg['To'] = env.DESTINATION_MAIL
    s = smtplib.SMTP(env.MAIL_SERVER)
    s.sendmail(msg['To'], [msg['From']], msg.as_string())
    s.quit()
    """
    print("Mail sent")

def print_missing_video(postId, title, videoId ):
    mail_text = ''
    mail_text = mail_text + 'PostId: ' + postId + '\n'
    mail_text = mail_text + 'Title:  ' + title + '\n'
    if videoId is not None:
        mail_text = mail_text + 'VideoId:' + videoId + '\n'
    mail_text = mail_text + '\n'
    sendmail_video("Video not found", mail_text)
    print(mail_text)

def process_map(videoMap, apikey,maxcount=5000, debug=False, days=3):
    count = 0
    for id, v in sorted(videoMap.items(),key=lambda x: x[1][2]):
        title, videoId, lastdate = v
        currentdate = datetime.date.fromtimestamp(time.time())
        delta = currentdate - lastdate
        if delta.days >= days:
            debug and print(title, videoId, lastdate)
            if title is not None:
                if videoId is not None:
                    validLink = youtube_tools.verify_link(title, videoId, apikey)
                    if not validLink:
                        print_missing_video(id, title, videoId )
                    else:
                        videoMap[id] = (title, videoId, datetime.date.fromtimestamp(time.time()))
        count = count+1
        if count > maxcount:
            return


parser = argparse.ArgumentParser()

parser.add_argument('--apikey')
parser.add_argument('--inputfile')
parser.add_argument('--maxcount')
parser.add_argument('--debug')
parser.add_argument('--days')

args = parser.parse_args()
debug = False if args.debug == None else True


with open(args.inputfile, 'rb') as handle:
    videoMap = pickle.load(handle)
    process_map(videoMap,args.apikey,maxcount=(int(args.maxcount) if args.days else 5000), debug=debug, days=(int(args.days) if args.days else 3) )

with open(args.inputfile, 'wb') as handle:
     pickle.dump(videoMap, handle,  protocol=pickle.HIGHEST_PROTOCOL)

