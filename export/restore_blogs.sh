pushd musicblogs/musicblogs
mongorestore -d musicblogs-ext .
mongo


# use musicblogs
# db.dropDatabase()
# db.copyDatabase("musicblogs-ext","musicblogs","localhost");
# use musicblogs-ext
# db.dropDatabase();