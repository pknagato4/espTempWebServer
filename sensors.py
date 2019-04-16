import ujson, onewire, ds18x20, dht
import utime as time
from machine import Pin


class SensorInterface:
    def measure(self):
        raise NotImplemented
    def get_measurement_as_str(self):
        raise NotImplemented


class DS18x20Sensor(SensorInterface):
    def __init__(self, pin):
        self.ds18x20 = ds18x20.DS18X20(onewire.OneWire(Pin(pin)))
        self.last_temp = None

    def measure(self):
        roms = self.ds18x20.scan()
        self.ds18x20.convert_temp()
        time.sleep_ms(750)
        self.last_temp = self.ds18x20.read_temp(roms[0])
        return self.last_temp

    def get_measurement_as_str(self):
        return 'Temperature: {}'.format(str(self.last_temp))


class DHTSensor(SensorInterface):
    def __init__(self, pin):
        self.dht = dht.DHT11(Pin(pin))

    def measure(self):
        self.dht.measure()
        return self.dht.temperature(), self.dht.humidity()

    def get_measurement_as_str(self):
        return 'Temperature: {} Humidity: {}'.format(str(self.dht.temperature()), str(self.dht.humidity()))


class Sensors:
    def __init__(self):
        self.sensors = []
        with open('sensors.json') as f:
            for sensor in ujson.load(f):
                if sensor['type'] == 'ds18x20':
                    self.sensors.append(DS18x20Sensor(sensor['pin']))
                elif sensor['type'] == 'dht':
                    self.sensors.append(DHTSensor(sensor['pin']))
                else:
                    print('Unknown sensor type: {}'.format(sensor['type']))

    def get_sensors(self):
        return self.sensors


