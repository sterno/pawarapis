import json

file_object = open("expenditures/zappa_template.json", "r")
cert_file = open("firebaseServiceAccountKey.json", "r")

zappa_json = json.load(file_object);
zappa_json["dev"]["environment_variables"]["cert"] = cert_file.read();

with open('expenditures/zappa_settings.json', 'w') as f:
    json.dump(zappa_json, f)
