from flask import Flask, request
from config_ import settings
import json
from common_utils.logger import logger
import common_utils.api_utils
from datetime import datetime
import os
import pickle
import requests
from note.note import NoteObject

app = Flask("main")

logger.info("Note Object is created.")


def process_note(status):
    if status == 'ok':
        try:
            note = NoteObject()

            lamp_number = 1
            bri = note.set_brightness_with_note()
            turn_on_off_signal = note.turn_on_off_with_note()

            note_dict = {"turn_on_off_signal": turn_on_off_signal, "bri": bri, "lamp_number": lamp_number}
            return note_dict
        except Exception as e:
            logger.error(e)
    else:
        return common_utils.api_utils.bad_request(f"Status is not ok.")



@app.route("/note", methods=["GET", "POST"])
def note_endpoint():
    status = request.args.get("status", None)

    if not status:
        return common_utils.api_utils.bad_request(f"Parameter 'status' must be provided.")

    if request.method == "POST":
        # post the okay signal
        # under construction
        update_date = datetime.now().strftime("%Y%m%d")
        return {
            "status": "ok",
            "update-date": update_date
        }

    note_dict = process_note(status)

    command = note_dict['bri'] if note_dict['bri'] else note_dict['turn_on_off_signal']
    lamp = note_dict['lamp_number']

    outfile = f"./output/note_dict"
    with open(outfile, 'wb') as pickle_file:
        pickle.dump(note_dict, pickle_file)

    return {"speech": command, "lamp": lamp}


if __name__ == "__main__":
    port = os.getenv("note-port", 5000)
    app.run(host="0.0.0.0", port=port, threaded=False)
