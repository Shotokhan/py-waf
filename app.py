from flask import Flask, Response, request
import requests
import json

app = Flask(__name__)

config = {}
config_path = "./volume/config.json"
with open(config_path, 'r') as f:
    config = json.load(f)

app_url = "http://{}:{}/".format(config['proxied_hostname'], config['proxied_port'])

def check_req(incoming_request):
    # fill this; here is an example
    user_agent = incoming_request.headers.get('User-Agent')
    if 'python' in user_agent:
        return False
    return True

def prohibit():
    res = Response("Internal Server Error", 500)
    return res


@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def catch_all(path):
    # this is very generic, but you can also use catch_all only for GET requests and define specific routes for your app for POST requests
    # TODO: handle /static route because it is considered "404 not found"
    if not check_req(request):
        return prohibit()
    headers = dict(request.headers)
    params = request.args or request.form or request.get_json(force=True, silent=True) or request.data
    try:
        params = dict(params)
    except ValueError:
        pass
    if request.method == 'GET':
        r = requests.get(app_url + path, headers=headers, params=params)
    elif request.method == 'POST':
        r = requests.post(app_url + path, headers=headers, data=params)    # TODO: how to know if you have to send a json
    else:
        return prohibit()
    r_headers = [(name, value) for (name, value) in r.raw.headers.items()]
    res = Response(r.content, r.status_code, headers)
    return res


if __name__ == '__main__':
    app.run(debug=config['debug'], host=config['waf_hostname'], port=config['waf_port'])
