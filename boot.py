import gc
import main
gc.collect()

mqtt_controller = main.MqttLedStripController()
mqtt_controller.subscribe(mqtt_controller.mqtt_callback)
while True:
    mqtt_controller.wait_for_msg()


