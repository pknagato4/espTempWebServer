import scripts
import neopixel
import machine
from umqtt.simple import MQTTClient as Client


class MqttLedStripController:
    def __init__(self):
        self.strip_length = 77
        self.np = neopixel.NeoPixel(machine.Pin(4), self.strip_length)
        self.config = self.load_config()
        self.client = Client(self.config['client_id'], self.config['broker'])

    @staticmethod
    def load_config():
        import ujson
        return ujson.load(open('config.json'))

    def mqtt_callback(self, topic, msg):
        msg = msg.decode("utf-8")
        print("Got msg for topic \"{}\" with body \"{}\"".format(topic, msg))
        if msg[0] == 'c':
            color = (int(msg[1:4]), int(msg[4:7]), int(msg[7:10]))
            for i in range(self.strip_length):
                self.np[i] = color
            self.np.write()
        elif msg[0] == '#':
            color = (int(msg[1:3], 16), int(msg[5:7], 16), int(msg[3:5], 16))
            for i in range(self.strip_length):
                self.np[i] = color
            self.np.write()
        elif msg[0] == 's':
            scripts.cleanLedStrip(self.np, self.strip_length)
            strip_len = int(msg[1:3])
            print("Set strip length to {}".format(strip_len))
        else:
            pass

    def wait_for_msg(self):
        print("Waiting for msg....")
        self.client.wait_msg()

    def subscribe(self, callback):
        while True:
            try:
                self.client.connect()
                self.client.set_callback(callback)
                self.client.subscribe('home/#')
                break
            except OSError:
                pass

