def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('ReykjavikOdbior', 'Haloanita69')
        while not sta_if.isconnected():
            pass
        ap_if = network.WLAN(network.AP_IF)
        ap_if.active(False)
    print('network config:', sta_if.ifconfig())


def get_temp():
    from machine import Pin
    import onewire, ds18x20, time
    ow = onewire.OneWire(Pin(5))
    ds = ds18x20.DS18X20(ow)

    roms = ds.scan()

    ds.convert_temp()
    time.sleep_ms(750)

    for rom in roms:
        return ds.read_temp(rom)


def publish_temp():
    import urequests, machine, ujson
    dict = {'espId': str(machine.unique_id()), 'value': str(get_temp())}
    encoded = ujson.dumps(dict)
    header = {'content-type': 'application/json'}
    resp = urequests.post("http://62.87.243.117:8000/api/temperatures/", data=encoded, headers=header)
    resp.close()
