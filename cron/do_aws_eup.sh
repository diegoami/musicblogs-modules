#!/bin/bash
source /home/ubuntu/miniconda3/bin/activate musicblogs
pushd /home/ubuntu/projects/musicblogs-scripts-PY/
/home/ubuntu/projects/musicblogs-scripts-PY/update_musicblogs.sh
/home/ubuntu/projects/musicblogs-scripts-PY/update_subtitles.sh
/home/ubuntu/projects/musicblogs-scripts-PY/verify_posts.sh 2>&1 > verification/verifications.txt
popd
pushd /home/ubuntu/projects/musicblogs-scripts-PY/export/
/usr/bin/mongodump -d musicblogs -o musicblogs
/usr/bin/git commit -a -m "Committing dump of musicblogs"
/usr/bin/git push
popd
pushd /home/ubuntu/projects/musicblogs-scripts-PY/verification/
/usr/bin/git commit -a -m "Committing verifications"
/usr/bin/git push origin
popd
/home/ubuntu/awscli/do_node.sh