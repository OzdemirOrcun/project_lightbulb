import json
import os
import asyncio
import aiohttp
import pickle
from datetime import datetime, timedelta
from common_utils.logger import logger
from common_utils import api_utils
from flask import Flask, request
from urllib.parse import urlencode
import glob

app = Flask(__name__)

only_safe_operations = os.getenv("only-safe-operations", "false")[0] == "t"

port = os.getenv("orchestrator-port", 8010)
note_port = os.getenv("note-port", 8011)
speech_port = os.getenv("speech-port", 8012)
bridge_port = os.getenv("bridge-port", 8013)

note_host = os.getenv("note-host", "localhost")
speech_host = os.getenv("speech-host", "localhost")
bridge_host = os.getenv("bridge-host", "localhost")

folder = "./output/"
if not os.path.exists(folder):
    os.makedirs(folder)


@app.route("/lightbulb", methods=["GET", "POST"])
def light_bulb_endpoint():
    request_data = request.get_json()
    logger.error(request_data)
    status = check_key(request_data, "status")
    manuel = check_key(request_data, "manuel")
    lamp = check_key(request_data, "lamp")

    if lamp is None:
        lamp = "1"

    if int(manuel) == 1:
        command = check_key(request_data, 'command')

        if command is None:
            return api_utils.bad_request("Please provide proper command")
        get_bridge_signal(command, lamp)

    else:
        try:
            status = status[0]
            logger.info(status)
        except Exception as e:
            logger.error(e)
            pass
        if status is None:
            return api_utils.bad_request("Please provide status speech/note")

        if status == 'speech':
            get_speech_signal()

            file_ = open("./output/speech_dict", 'rb')
            the_speech = pickle.load(file_)
            file_.close()

            get_bridge_signal(the_speech["speech"], the_speech["lamp"])

        elif status == 'note':

            # TODO: pickle the note up
            the_note = get_note_signal()
            get_bridge_signal(the_note, lamp)

    return "lightbulb_experience"


def get_bridge_signal(command, lamp):
    url = build_url(bridge_host, bridge_port, "bridge",
                    {"command": command, "lamp": lamp, "status": "ok"})
    return asyncio.run(async_get_request(url))


def get_note_signal():
    url = build_url(note_host, note_port, "note",
                    {"status": "ok"})
    return asyncio.run(async_get_request(url))


def get_speech_signal():
    url = build_url(speech_host, speech_port, "speech",
                    {"status": "ok"})
    return asyncio.run(async_get_request(url))


def build_url(hostname, specified_port, path, url_vars):
    return f"http://{hostname}:{specified_port}/{path}?{urlencode(url_vars)}"


def check_key(dict_, key):
    """ Checks dict key, if not exits return None """
    try:
        return dict_[key]
    except KeyError as e:
        logger.error(e)
        return None


async def async_get_request(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=None) as resp:
            return await resp.json(content_type=None)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)
