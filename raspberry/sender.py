#!/usr/bin/env python3

import os
import rfid
import RPi.GPIO as GPIO
import time
import datetime
import paho.mqtt.client as mqtt
import json
import board
import busio
import adafruit_bme280
from typing import Optional
from card_handler import rfid_read

terminal_id = "T0"
broker = "10.0.0.1"

client = mqtt.Client()

uid: Optional[int] = None
num: Optional[int] = None
buzzerPin = 18
buttonRed = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzerPin, GPIO.OUT)
GPIO.setup(buttonRed, GPIO.IN, pull_up_down=GPIO.PUD_UP)


class WeatherSensor:
    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.__sensor = adafruit_bme280.Adafruit_BME280_I2C(i2c, 0x76)
        self.__init_env()

    def __init_env(self):
        self.__sensor.sea_level_pressure = 1013.25
        self.__sensor.standby_period = adafruit_bme280.STANDBY_TC_500
        self.__sensor.iir_filter = adafruit_bme280.IIR_FILTER_X16
        self.__sensor.overscan_pressure = adafruit_bme280.OVERSCAN_X16
        self.__sensor.overscan_humidity = adafruit_bme280.OVERSCAN_X1
        self.__sensor.overscan_temperature = adafruit_bme280.OVERSCAN_X2

    def get_weather_data(self):
        return {
            "temperature": self.__sensor.temperature,
            "humidity": self.__sensor.humidity,
            "pressure": self.__sensor.pressure,
            "altitude": self.__sensor.altitude,
        }


weather_handler = WeatherSensor()


def connect_to_broker() -> None:
    client.connect(broker)
    client.publish("status", "Raspberry Pi connected")


def disconnect_from_broker() -> None:
    client.publish("status", "Raspberry Pi disconnected")
    client.disconnect()


def call_rfid_reading(uid, num) -> None:
    message = {"uid": uid, "num": num, "timestamp": datetime.datetime.now().isoformat()}
    client.publish("response/rfid", json.dumps(message))


def send_weather_data() -> None:
    try:
        weather_data = weather_handler.get_weather_data()
        weather_data["timestamp"] = datetime.datetime.now().isoformat()
        client.publish("sensors/weather", json.dumps(weather_data))
        print(f"Weather data sent: {weather_data}")
    except Exception as e:
        client.publish("sensors/weather", json.dumps({"error": str(e)}))
        print(f"Error reading weather data: {e}")


def buzzer(state) -> None:
    GPIO.output(buzzerPin, not state)


def stop() -> None:
    GPIO.cleanup()
    disconnect_from_broker()
    os._exit(0)


def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with result code {rc}")
    client.subscribe("command/rfid")
    client.subscribe("command/weather")


def on_message(client, userdata, msg):
    global uid, num
    topic = msg.topic
    payload = json.loads(msg.payload.decode())
    print(f"Received message on topic {topic}: {payload}")

    if topic == "command/rfid" and payload.get("action") == "start_rfid":
        print("Starting RFID listener...")
        try:
            uid, num = rfid_read()
            call_rfid_reading(str(uid), str(num))

            buzzer(True)
            time.sleep(0.5)
            buzzer(False)
            time.sleep(0.5)

        except Exception as e:
            client.publish("response/rfid", json.dumps({"error": str(e)}))
            print(f"Error during RFID read: {e}")

    elif topic == "command/weather" and payload.get("action") == "get_weather":
        print("Sending weather data...")
        send_weather_data()


def run_sender() -> None:
    GPIO.add_event_detect(
        buttonRed, GPIO.FALLING, callback=lambda x: stop(), bouncetime=200
    )

    client.on_connect = on_connect
    client.on_message = on_message

    connect_to_broker()

    try:
        client.loop_forever()
    except KeyboardInterrupt:
        stop()


if __name__ == "__main__":
    run_sender()
