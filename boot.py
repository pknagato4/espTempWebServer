import gc, core
from main import WebServer
gc.collect()

core.do_connect()
ws = WebServer()
ws.start_led_server()
