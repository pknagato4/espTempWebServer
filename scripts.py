import colorsys
import utime

def moveArrByOneForward(arr, length):
    for i in reversed(range(length)):
        if i > 1:
            arr[i] = arr[i-1]
        else:
            arr[1] = arr[0]


def travelingStrip(np, length):
    for l, r in zip(range(length), (1, 0.1, 0, 0.5, 0.0, 0.0, 0.3, 0.6, 0.9, 0.6)):
        r, g, b = colorsys.hsv_to_rgb(180/360, 1, r)
        np[0] = (int(r*255), int(g*255), int(b*255))
        moveArrByOneForward(np, length)
        np[l] = (0, 0, 0)
        np.write()


def travelingDot(np, length):
    np[0] = (255, 0, 0)
    for l in range(length):
        moveArrByOneForward(np, length)
        np[l] = (0, 0, 0)
        np.write()
    utime.sleep_ms(500)


def rainbowDemo2(np, length):
    for c, l in zip(range(1, 36, 1), range(1, 100, int(36/10))):
        r, g, b = colorsys.hsv_to_rgb(c / 36, 1, 0.1)
        moveArrByOneForward(np, length)
        np[0] = (int(r*255), int(g*255), int(b*255))
        np.write()


def rainbowDemo(np, length):
    for c in range(0, 360, 10):
        for i in range(length):
            r, g, b = colorsys.hsv_to_rgb(c / 360, 1, 0.1)
            np[i] = (int(r*255), int(g*255), int(b*255))
        np.write()


def anotherRainbowDemo(np, length):
    for c in range(360):
        r, g, b = colorsys.hsv_to_rgb(c / 360, 1, 0.1)
        np[c % length] = (int(r * 255), int(g * 255), int(b * 255))
        np.write()


def cleanLedStrip(np, length):
    for i in range(length):
        np[i] = (0, 0, 0)
    np.write()
