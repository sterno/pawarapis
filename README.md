# Pawar APIs

Based off [zouzias](https://github.com/zouzias)/[docker-compose-flask-example](https://github.com/zouzias/docker-compose-flask-example).


## Note on the firebase key

We're using the firebase admin interface so to generate a new key, go to the IAM and admin portion of the Google cloud console (there's a link on the gear menu on the left column of the firebase console) and go to Service Accounts. You can generate a new user on there and make sure it has access to databases.

Once you have the key, name it firebaseServiceAccountKey.json and copy it into the expenditures directory. (It will be ignored by git.) Then, when you start up docker it copies that file into /code with everything else.
