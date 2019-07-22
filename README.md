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

* client_secrets.json (blogger + youtube)
* amara.amara_env.py: copy from amara.amara_env_template.py and put your API-KEY there


## Update blogs entries

A mongodb instance should be running. Execute

* ./update_posts.sh ( --no-update_subtitles )


## Create new entries in amara

```
python create_entry_for_amara.py --blogId <blogId> --postId <postId> --language_code <language_code>
```


