import RPi.GPIO as IO
import time


def PMMsetup(pin, freq):
    
    IO.setwarnings(False)
    IO.setmode(IO.BCM)
    IO.setup(pin, IO.OUT)

    p = IO.PWM(pin, freq)
    p.start(0)

    voltage = [0]
    times = [0]

    cap = 75
    t = 0
    while True:
        for x in range(cap):
            t = t + 0.1
            times.append(t)
            voltage.append(x)
            p.ChangeDutyCycle(x)
            time.sleep(0.1)
        for x in range(cap):
            t = t + 0.1
            times.append(t)
            voltage.append(x*3.3/100)
            p.ChangeDutyCycle(cap-x)
            time.sleep(0.1)
