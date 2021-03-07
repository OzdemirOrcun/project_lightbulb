from flask import Flask, request
from config_ import settings
from common_utils.logger import logger
import common_utils.api_utils
from datetime import datetime
import os
from bridge.bridge import Bridge_Object

app = Flask("main")

IP_ADRESS = settings.local_ip_adress

b = Bridge_Object(ip_adress=IP_ADRESS)
bridge = b.connect_bridge()
logger.info("Bridge object is created.")


def process_bridge(status, command, lamp):
    if status == 'ok':

        percentage = None
        try:
            percentage = int(command)
        except Exception as e:
            print(e)
        if percentage:
            b.set_brightness(bridge, percentage, lamp=int(lamp))
            logger.info(f"brightness is set to {percentage}%.")
        if "on" in command:
            b.turn_on_lights(bridge, lamp=int(lamp))
            logger.info("lights are on")
        elif "off" in command:
            b.turn_off_lights(bridge, lamp=int(lamp))
            logger.info("lights are off")

    else:
        return common_utils.api_utils.bad_request(f"Status is not ok.")


@app.route("/bridge", methods=["GET", "POST"])
def bridge_endpoint():
    status = request.args.get("status", None)
    command = request.args.get("command", None)
    lamp = request.args.get("lamp", 1)

    if not command:
        return common_utils.api_utils.bad_request(f"Parameter 'command' must be provided.")

    if request.method == "POST":
        # post the okay signal
        # under construction
        update_date = datetime.now().strftime("%Y%m%d")
        return {
            "status": "ok",
            "update-date": update_date
        }

    process_bridge(status, command, lamp)
    return {"command": command, "lamp": lamp}


if __name__ == "__main__":
    port = os.getenv("bridge-port", 5000)
    app.run(host="0.0.0.0", port=port, threaded=False)
