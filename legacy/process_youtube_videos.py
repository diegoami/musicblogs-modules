import csv
import sys
import smtplib
from email.mime.text import MIMEText

import youtube_tools
import blogspot_tools
import environment as env

missing_videos = []


def sendmail_success(subject,text):
    print("Now sending mail....")
    msg = MIMEText(text,_charset ='utf-8')
    msg['Subject'] = subject
    msg['From'] = env.DESTINATION_MAIL
    msg['To'] = env.DESTINATION_MAIL
    s = smtplib.SMTP(env.MAIL_SERVER)
    s.sendmail(msg['To'], [msg['From']], msg.as_string())
    s.quit()
    print("Mail sent")


def process_videos_in_blog(blogId, apikey):
    print("Now parsing blog "+blogId+" with key "+apikey)
    for blog_post in blogspot_tools.iterate_blog_posts(blogId, apikey):
        for postId, title, videoId in blogspot_tools.iterate_title_and_videos(blog_post, apikey):
            proc_tuple = (blogId, postId,  title, videoId)
            if title is not None:
                if videoId is not None:
                    validLink = youtube_tools.verify_link(title, videoId, apikey)
                    if not validLink:
                        missing_videos.append(proc_tuple)

                else:
                    missing_videos.append(proc_tuple)


if len(sys.argv) < 2:
    print("Usage : python list_youtube_videos.py <blogsfile.txt>")
    print("Each row must be in the form blogid,apikey")
    sys.exit(0)
else:
    filename= sys.argv[1]




with open(filename, 'r') as csvfile:
    mail_text = ""
    reader = csv.reader(csvfile)
    for row in reader:
        if len(row) < 2:
            print("Each row must be in the form blogid,apikey")
            print("Skipping....")
        else:
            process_videos_in_blog(row[0], row[1])

    for blogId,postId,title,videoId in missing_videos:
        mail_text = mail_text + 'BlogId: ' + blogId + '\n'
        mail_text = mail_text + 'PostId: ' + postId + '\n'
        mail_text = mail_text + 'Title:  '  + title + '\n'
        if videoId is not None:
            mail_text = mail_text + 'VideoId:' + videoId + '\n'
        mail_text = mail_text + '\n'
    sendmail_success("Videos not found", mail_text)
