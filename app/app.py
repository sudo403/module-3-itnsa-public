from flask import Flask, jsonify
import uuid
import yaml
import os

app = Flask(__name__)

yaml_struct = {"server": {"addr": "127.0.0.1", "port": 1234, "files_folder": "./data"}
               }


@app.route("/app")
def app_check():
    data = {"value": uuid.uuid4()}
    try:
        with open(evariables['server']['files_folder'] + "/" + os.popen("hostname").read() + "-" + str(data['value']), 'w+') as file:
            data["additional_info"] = "File created"
            file.write(yaml.dump(data, default_flow_style=False))
    except FileNotFoundError:
        print("dir not found")
        data["additional_info"] = "Directory that wrote in config not exists"

    return data

@app.route("/")
def main_page():
    hostname = os.popen('hostname').read()
    ls = os.listdir(os.getcwd() + "/" + (evariables['server']['files_folder']))
    return jsonify({"hostname": hostname, "COMPETITOR_ID": os.getenv('COMPETITOR_ID'),"listdir": ls})

@app.route("/health")
def healthcheck():
    return "Healthy"

@app.route("/variable")
def check_var():
    return os.getenv('COMPETITOR_ID')

if __name__ == '__main__':
    try:
        with open("./env.yml") as file:
            evariables = yaml.safe_load(file)
    except:
        print("There is no env.yml, creating\n")
        f = open("./env.yml", 'w+')
        output = yaml.dump(yaml_struct, default_flow_style=False)
        print(output)
        f.write(output)
        f.close()
        with open("./env.yml") as file:
            evariables = yaml.safe_load(file)

    app.run(host = evariables['server']['addr'], port=evariables['server']['port'], debug=False)