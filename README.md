# Pawar APIs

Based off [zouzias](https://github.com/zouzias)/[docker-compose-flask-example](https://github.com/zouzias/docker-compose-flask-example).

## Deploy

This package has been set up to be able to deploy using AWS Lambda.  To deploy, do the following:

1. Configure your AWS setup locally with a user that has appropriate rights to deploy the API
gateway, Lambda, etc.  A user with the "lambda_deploy" group in IAM can deploy
2. Put a copy of the firebaseSeviceAccountKey.json in this directory (see below for details)
3. Run the script lambda_deploy.sh

When the script runs it will initialize a virtualenv, install the appropriate packages, and then
install/run [zappa](https://github.com/Miserlou/Zappa).  It will also assemble the JSON config
for zapp, including the certificate needed to authenticate to firebase.

After the script has run, it will clean up after itself, removing the virtualenv, and other temporary
files.  No muss.  No fuss.

Questions about how the deploy works?  Talk to Steve (steve_stearns on the digital team Slack)

## Note on the firebase key

We're using the firebase admin interface so to generate a new key, go to the IAM and admin portion of the Google cloud
console (there's a link on the gear menu on the left column of the firebase console) and go to Service Accounts.
You can generate a new user on there and make sure it has access to databases.

Once you have the key, name it firebaseServiceAccountKey.json and copy it into the expenditures directory.
(It will be ignored by git.) Then, when you start up docker it copies that file into /code with everything else.
