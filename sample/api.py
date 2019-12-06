from copy import deepcopy

from flask import Flask
from flask import jsonify
from flask import request
import urllib.request
import json
import threading

threadLock = threading.Lock()
UNIQUE_GAME_ID = 0
app = Flask(__name__)


@app.route('/api/')
def hello():
    return jsonify("test")


@app.route('/api/get_message', methods=['POST'])
def get_message():
    """
    Function to query a chatbot getting the user id, the bot id (what bot should I query ?)
    and the message from the user.
    It returns the chatbot anwser in json format.
    """
    # get params from the POST request
    # try
    print("zeeeeeeeeeeeeeee", request.data.decode())
    user_id = request.json['user_id']
    bot_id = request.json['bot_id']  # ex: 5005
    message = request.json['message']
    # query the concerned bot
    bot_url = "http://localhost:" + str(bot_id) + "/webhooks/rest/webhook"
    params = {"sender": user_id, "message": message}
    result = http_json_request(params, bot_url)
    new_msg = ""
    pile_run = deepcopy(result)
    while len(pile_run) > 0:
        msg = pile_run.pop(0)
        if "buttons" in msg:
            params["message"] = msg["buttons"][0]["payload"]
            pile_run.extend(http_json_request(params, bot_url))
        elif "custom" in msg:
            message += "<{}>\n".format(msg["custom"]["type"])
        else:
            new_msg += "{}\n".format(msg["text"])
    return new_msg
    # except Exception as err:
    #     print("Erreur dans get_message() :", err)
    #     return "Error"


@app.route('/api/get_id', methods=['GET'])
def get_id():
    """
    Returns an id that's ensured to be unique
    """
    global UNIQUE_GAME_ID
    with threadLock:
        UNIQUE_GAME_ID += 1
    return str(UNIQUE_GAME_ID)


def http_json_request(json_data, url, method="POST"):
    """
    Function to make http json request
    :param json_data: (dict) json to send
    :param url: (string) url to send the json
    :param method: (string) method of the request (POST, PUT, ...)
    :return: (dic) Answer of the request in json format
    """
    try:
        req = urllib.request.Request(url, method=method)
        # Add the json header
        req.add_header('Content-Type', 'application/json; charset=utf-8')
        # Encode the json data
        json_string_encode = json.dumps(json_data).encode("utf-8")
        req.add_header('Content-Length', len(json_string_encode))
        # Send the request
        response = urllib.request.urlopen(req, json_string_encode)
        # Get the json response
        data = response.read()
        # Get the encoding
        encoding = response.info().get_content_charset('utf-8')
        return json.loads(data.decode(encoding))
    except Exception as e:
        error_msg = "Error in the http request {}: {}".format(url, e)
        print(error_msg)
        return None
