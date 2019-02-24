pushd musicblogs/musicblogs
mongoimport -d musicblogs-ext .
mongo
# db.copyDatabase("musicblogs-ext","musicblogs","localhost");
# use musicblogs-ext
# db.dropDatabase();