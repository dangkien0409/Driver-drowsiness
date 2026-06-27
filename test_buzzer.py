#!/usr/bin/env python3
"""
Short utility to pulse the configured BUZZER_PIN for testing.
Usage: python3 test_buzzer.py
"""
import time
import config
from importlib import import_module

try:
    GPIO = import_module('Jetson.GPIO')
except Exception as e:
    print('Jetson.GPIO not available:', e)
    GPIO = None

pin = getattr(config, 'BUZZER_PIN', None)
if pin is None:
    print('BUZZER_PIN not set in config.py')
    raise SystemExit(1)

active_low = bool(getattr(config, 'BUZZER_ACTIVE_LOW', False))
active_state = None
idle_state = None

if GPIO is None:
    print('GPIO module not available. Cannot test hardware.')
    raise SystemExit(1)

try:
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)
    active_state = GPIO.LOW if active_low else GPIO.HIGH
    idle_state = GPIO.HIGH if active_low else GPIO.LOW
    GPIO.output(pin, idle_state)

    print(f'Pulsing buzzer on BOARD pin {pin} (active_low={active_low})')
    for i in range(5):
        GPIO.output(pin, active_state)
        time.sleep(0.2)
        GPIO.output(pin, idle_state)
        time.sleep(0.2)

    print('Done pulsing')

except Exception as e:
    print('Error while testing buzzer:', e)

finally:
    try:
        GPIO.output(pin, idle_state)
        GPIO.cleanup(pin)
    except Exception:
        pass
