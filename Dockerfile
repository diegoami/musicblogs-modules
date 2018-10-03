FROM alpine:3.7
RUN apk add --no-cache --virtual .build-deps g++ python3-dev libffi-dev openssl-dev
RUN apk add --no-cache --update python3
RUN pip3 install --upgrade pip setuptools
RUN apk add --no-cache --virtual bash vim
RUN mkdir opt
ADD requirements.txt /opt
RUN pip install -r /opt/requirements.txt
ADD legacy /opt/legacy
ADD amara /opt/amara
ADD tools /opt/tools
ADD create_entry_for_amara.py /opt
ADD list_posts.py /opt
ADD ui_create_amara.py /opt
ADD update_subtitles.py /opt
ADD update_musicblogs.sh /opt
RUN cd /opt