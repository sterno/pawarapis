#!/bin/sh

# Specify the python and pip command paths
PIP=pip3

# Install VirtualEnv for the project

declare -a cmdArgs='([0]=$PIP [1]="install virtualenv")'
${cmdArgs[@]}
virtualenv expenditures
source expenditures/bin/activate

# Install packages
pip install zappa
pip install flask
pip install flask_cors
pip install boto3
pip install firebase_admin

# Start Zappa Update
python appendFirebaseCert.py
cd expenditures

if zappa deploy; then
    echo "Zappa Deploy Done"
else
    zappa update
    echo "Zappa Update Done"
fi

# Cleanup
deactivate
rm -rf lib/ include/ bin/ pip-selfcheck.json
rm zappa_settings.json

cd ..