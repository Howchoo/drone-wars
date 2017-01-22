#!/usr/bin/env python
# Note: run pigpiod as sudo in the background

import time

import pigpio

GPIO=4
NONE=0

pigpio.start()

pigpio.set_mode(GPIO, pigpio.OUTPUT)

wf=[]

# 100 kHz clock: 4 usec high, and 6 usec low
wf.append(pigpio.pulse(gpio_on=(1<<GPIO), gpio_off=NONE, delay=4))
wf.append(pigpio.pulse(gpio_on=NONE, gpio_off=(1<<GPIO), delay=6))

pigpio.wave_clear()

pigpio.wave_add_generic(wf)

# go until stopped by a control-c
# actually, this ends right away if I don't put the sleep.
# Is it because pigpio is doing the waveform?
try:
    print 'wave tx repeat'
    pigpio.wave_tx_repeat()
    time.sleep(999)

except KeyboardInterrupt:
    print 'wave tx interrupt'
    pigpio.wave_tx_stop()

    pigpio.stop()