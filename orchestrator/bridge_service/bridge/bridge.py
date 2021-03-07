from phue import Bridge
from config_ import settings
from common_utils.logger import logger

IP_ADRESS = settings.local_ip_adress

class Bridge_Object:
    def __init__(self, ip_adress=None):

        if ip_adress is None:
            self.ip_adress = IP_ADRESS
        else:
            self.ip_adress = ip_adress

        self.name = None
        self.number_of_devices = None
        self.connected = False

    def connect_bridge(self, verbose=0):
        b = Bridge(self.ip_adress)
        try:
            b.connect()
            logger.info("Bridge is connected.")
            self.connected = True
            if verbose == 1:
                logger.info(b.get_api())
            logger.info(f"The light is on: {b.get_light(1, 'on')}")
            return b
        except Exception as e:
            logger.error("Bridge is not connected", e)
            return None

    def turn_on_lights(self, bridge, lamp=1):
        lights = bridge.get_light_objects('id')
        self.number_of_devices = len(lights)
        lights[lamp].on = True

    def turn_off_lights(self, bridge, lamp=1):
        lights = bridge.get_light_objects('id')
        self.number_of_devices = len(lights)
        lights[lamp].on = False

    def set_brightness(self, bridge, percentage, lamp=1):
        lights = bridge.get_light_objects('id')
        bri = round(254 * (percentage / 100))
        self.number_of_devices = len(lights)
        lights[lamp].brightness = bri
