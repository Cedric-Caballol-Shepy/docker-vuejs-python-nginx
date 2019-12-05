from flask import Flask
from flask import jsonify
from flask import request
import urllib.request
import json

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
    user_id = request.form['user_id']
    bot_id = request.form['bot_id']  # ex: 5005
    message = request.form['message']
    # query the concerned bot
    bot_url = "http://localhost:" + bot_id + "/webhooks/rest/webhook"
    params = {"sender": user_id, "message": message}
    result = jsonify(http_json_request(params, bot_url))
    return result


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
