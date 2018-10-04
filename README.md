# musicblogs-scripts-PY

Collection of scripts simplifying the maintainance of my music blogs

* http://russianlyrics.blogspot.com/
* http://polishlyrics.blogspot.com/
* http://easterneuropelyrics.blogspot.de/
* http://frenchmusiclyrics.blogspot.com/
* http://southslaviclyrics.blogspot.com/
* http://romanianlyrics.blogspot.com/
* http://italianlyrics.blogspot.com/

Including subtitles using http://www.amara.org .

Also used to fill the database for http://www.europoplyrics.com .

## Credential needed

* client_secrets_yt.json (youtube)
* client_secrets.json (blogger)

## Update blogs entries

A mongodb instance should be running. Execute

* ./update_musicblog.sh
* ./update_subtitles.sh


## Create new entries in amara

```
python create_entry_for_amara.py --blogId <blogId> --postId <postId> --language_code <language_code>
```

.env and client_secrets.json

## Docker file

docker build -f Dockerfile -t diegoami/musicblog_scripts:latest .
export CWD=$(pwd)
docker run -v $CWD/.env:/opt/.env -v $CWD/client_secrets.json:/opt/client_secrets.json -v $CWD/blogger.dat:/opt/blogger.dat -it diegoami/musicblog_scripts:latest bash

docker run -p 5001:5001 -v $CWD/.env:/opt/.env -v $CWD/client_secrets.json:/opt/client_secrets.json -v $CWD/blogger.dat:/opt/blogger.dat -it diegoami/musicblog_scripts:latest