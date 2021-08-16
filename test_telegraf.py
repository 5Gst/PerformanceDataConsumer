from flask import Flask, request
import configparser
import os

config = configparser.ConfigParser()
config.read('settings.ini')
defconf = config['DEFAULT']

def set_variable(name):
    env_var = os.environ.get(name)
    if env_var:
        return env_var
    else:
        return defconf[name]

TELEGRAF_HOST = set_variable('PDC_TELEGRAF_HOST')
TELEGRAF_PORT = set_variable('PDC_TELEGRAF_PORT')

app = Flask(__name__)

@app.route('/telegraf', methods=['POST'])
def get_metrics():
    if not request.is_json:
        return '', 404
    info = request.get_json()
    print(info)
    return '', 200


if __name__ == '__main__':
    app.run(host=TELEGRAF_HOST, port=TELEGRAF_PORT)