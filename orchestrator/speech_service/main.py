from flask import Flask, request
from config_ import settings
import json
from common_utils.logger import logger
import common_utils.api_utils
from datetime import datetime
import os
import requests
from speech_service.speech.speech import SpeechObject

app = Flask("main")


logger.info("Speech Object is created.")


def process_speech(status, sentence_from_google):
    if status == 'ok':

        try:
            speech = SpeechObject(sentence_from_google)

            lamp_number = speech.get_lamp_number()
            bri = speech.set_brightness_with_speech()
            turn_on_off_signal = speech.turn_on_off_with_speech()

            speech_dict = {"turn_on_off_signal": turn_on_off_signal, "bri": bri, "lamp_number": lamp_number}
            return speech_dict
        except Exception as e:
            logger.error(e)
    else:
        return common_utils.api_utils.bad_request(f"Status is not ok.")


@app.route("/speech", methods=["GET", "POST"])
def speech_endpoint():

    # TODO : Speech should not be an argument for this request, request should be called then retrieve speech from
    #  google

    resp = requests.get('https://api-v1.lightbulb.com/sentence?filter[stop]=speech')
    text_from_ga = resp.json()['data']

    status = request.args.get("status", None)

    if not status:
        return common_utils.api_utils.bad_request(f"Parameter 'status' must be provided.")

    if request.method == "POST":
        update_date = datetime.now().strftime("%Y%m%d")

        response = {
            "expectUserResponse": False,
            "status": "ok",
            "finalResponse": {
                "richResponse": {
                    "items": [
                        {
                            "simpleResponse": {
                                'ssml': f'<speak>{update_date}</speak>'
                            }
                        }
                    ]
                }
            }
        }

        response_text = json.dumps(response, indent=2, sort_keys=True)
        return response_text, 200

    speech_dict = process_speech(status, text_from_ga)

    command = speech_dict['bri'] if speech_dict['bri'] else speech_dict['turn_on_off_signal']
    lamp = speech_dict['lamp_number']

    return {"speech": command, "lamp": lamp}


if __name__ == "__main__":
    port = os.getenv("speech-port", 5000)
    app.run(host="0.0.0.0", port=port, threaded=False)
