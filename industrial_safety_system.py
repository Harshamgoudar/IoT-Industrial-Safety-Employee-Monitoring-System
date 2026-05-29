```python id="r1kvfa"
# =====================================================
# IoT-Based Smart Industrial Safety Monitoring System
# Raspberry Pi 4 + Gas Sensor + Flame Sensor
# Developed By: Harsha Muttanna Goudar
# =====================================================

import RPi.GPIO as GPIO
import time
import requests

# =====================================================
# GPIO PIN SETUP
# =====================================================

gas_sensor = 17
flame_sensor = 27

buzzer = 22
red_led = 23
green_led = 24
relay = 25

# =====================================================
# UBIDOTS CONFIGURATION
# =====================================================

TOKEN = "YOUR_UBIDOTS_TOKEN"

url = "https://industrial.api.ubidots.com/api/v1.6/devices/industrial_safety_system"

headers = {
    "X-Auth-Token": TOKEN,
    "Content-Type": "application/json"
}

# =====================================================
# GPIO MODE
# =====================================================

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(gas_sensor, GPIO.IN)
GPIO.setup(flame_sensor, GPIO.IN)

GPIO.setup(buzzer, GPIO.OUT)
GPIO.setup(red_led, GPIO.OUT)
GPIO.setup(green_led, GPIO.OUT)
GPIO.setup(relay, GPIO.OUT)

# =====================================================
# INITIAL STATE
# =====================================================

GPIO.output(buzzer, GPIO.LOW)
GPIO.output(red_led, GPIO.LOW)
GPIO.output(green_led, GPIO.HIGH)
GPIO.output(relay, GPIO.HIGH)

print("===================================")
print(" SMART INDUSTRIAL SAFETY SYSTEM ")
print("===================================")

# =====================================================
# MAIN LOOP
# =====================================================

try:

    while True:

        gas_value = GPIO.input(gas_sensor)
        flame_value = GPIO.input(flame_sensor)

        print("\nChecking Industrial Environment...")

        # =============================================
        # GAS LEAKAGE DETECTION
        # =============================================

        if gas_value == 0:

            print("WARNING : GAS LEAKAGE DETECTED")

            GPIO.output(buzzer, GPIO.HIGH)
            GPIO.output(red_led, GPIO.HIGH)
            GPIO.output(green_led, GPIO.LOW)

            GPIO.output(relay, GPIO.LOW)

            data = {
                "gas_sensor": 1,
                "flame_sensor": 0,
                "status": 1
            }

            response = requests.post(
                url,
                headers=headers,
                json=data
            )

            print("Data Uploaded to Ubidots")

        # =============================================
        # FIRE DETECTION
        # =============================================

        elif flame_value == 0:

            print("WARNING : FIRE DETECTED")

            GPIO.output(buzzer, GPIO.HIGH)
            GPIO.output(red_led, GPIO.HIGH)
            GPIO.output(green_led, GPIO.LOW)

            GPIO.output(relay, GPIO.LOW)

            data = {
                "gas_sensor": 0,
                "flame_sensor": 1,
                "status": 2
            }

            response = requests.post(
                url,
                headers=headers,
                json=data
            )

            print("Fire Alert Uploaded")

        # =============================================
        # NORMAL CONDITION
        # =============================================

        else:

            print("SYSTEM STATUS : NORMAL")

            GPIO.output(buzzer, GPIO.LOW)
            GPIO.output(red_led, GPIO.LOW)
            GPIO.output(green_led, GPIO.HIGH)

            GPIO.output(relay, GPIO.HIGH)

            data = {
                "gas_sensor": 0,
                "flame_sensor": 0,
                "status": 0
            }

            response = requests.post(
                url,
                headers=headers,
                json=data
            )

            print("Normal Data Uploaded")

        time.sleep(2)



except KeyboardInterrupt:

    print("\nSystem Stopped")

    GPIO.cleanup()
