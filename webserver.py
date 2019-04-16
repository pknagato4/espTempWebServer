import usocket as socket
import sensors
import ujson
import utime as time


class WebServer:
    def __init__(self):
        self.sensors = sensors.Sensors()

    def get_measurements(self):
        measurement = []
        for sensor in self.sensors.get_sensors():
            sensor.measure()
            measurement.append(sensor.get_measurement_as_str())
        return measurement

    def get_sensor_measurements(self):
        meas = ""
        for measurement in self.get_measurements():
            meas += """<p>Current temperature: """ + str(measurement) + """</p><br>"""
        return meas

    def web_page(self):
        temperature_info = self.get_sensor_measurements()

        html = """
        <html>
            <head>
                <title>ESP Web Server</title>
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <link rel="icon" href="data:,"> 
                <style>
                    html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
                    h1{color: #0F3376; padding: 2vh;}
                    p{font-size: 1.5rem;}
                    .button{display: inline-block; background-color: #e7bd3b; border: none; 
                            border-radius: 4px; color: white; padding: 16px 40px;
                            text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
                </style>
            </head>
            <body>
                <h1>ESP Temperature Server</h1> 
                """ + temperature_info + """ 
                <p>
                    <a href="/?temperature"><button class="button">Check temperature</button></a>
                </p>
            </body>
        </html>"""
        return html

    def handle_request(self, request):
        temp = request.find('/?temperature')
        is_temp_get = request.find('/get/temperature')
        if temp != -1:

        if is_temp_get != -1:
            val = {"value": self.ds_temperature}
            response, header = ujson.dumps(val), 'Content-Type: application/json\n'
        else:
            response, header = self.web_page(), 'Content-Type: text/html\n'
        return response, header

    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', 80))
        s.listen(5)

        while True:
            try:
                conn, addr = s.accept()
                print('Got a connection from %s' % str(addr))
                request = conn.recv(1024)
                request = str(request)
                print('Content = %s' % request)
                response, header = self.handle_request(request)
                conn.send('HTTP/1.1 200 OK\n')
                conn.send(header)
                conn.send('Connection: close\n\n')
                conn.sendall(response)
                conn.close()
            except OSError as e:
                print("Got exception ", str(e), "pass...")
                pass

