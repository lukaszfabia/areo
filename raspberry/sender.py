import threading
import os
import RPi.GPIO as GPIO
import time
import datetime
import paho.mqtt.client as mqtt
import json
from typing import Optional
from handlers import WeatherHandler
from mfrc522 import MFRC522

terminal_id = "T0"
broker = "10.108.33.124"
port = 1883

client = mqtt.Client()

uid: Optional[int] = None
num: Optional[int] = None
buzzerPin = 23
buttonRed = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzerPin, GPIO.OUT)
GPIO.setup(buttonRed, GPIO.IN, pull_up_down=GPIO.PUD_UP)

rfid_reader = MFRC522()
weather_handler = WeatherHandler()

rfid_listening = False


def connect_to_broker() -> None:
    client.connect(broker, port=port, keepalive=60)
    client.publish("status", "Raspberry Pi connected")


def disconnect_from_broker() -> None:
    client.publish("status", "Raspberry Pi disconnected")
    client.disconnect()


def call_rfid_reading(uid, num) -> None:
    message = {"uid": uid, "num": num, "timestamp": datetime.datetime.now().isoformat()}
    client.publish("response/rfid", json.dumps(message))


def send_weather_data() -> None:
    try:
        weather_data = weather_handler.get_weather()
        weather_data["timestamp"] = datetime.datetime.now().isoformat()
        client.publish("response/weather", json.dumps(weather_data))
        print(f"Weather data sent: {weather_data}")
    except Exception as e:
        client.publish("response/weather", json.dumps({"error": str(e)}))
        print(f"Error reading weather data: {e}")


def buzzer(state) -> None:
    GPIO.output(buzzerPin, not state)


def stop() -> None:
    GPIO.cleanup()
    disconnect_from_broker()
    os._exit(0)


def rfid_listener():
    global rfid_listening, uid, num
    while rfid_listening:
        try:
            (status, TagType) = rfid_reader.MFRC522_Request(rfid_reader.PICC_REQIDL)
            if status == rfid_reader.MI_OK:
                (status, raw_uid) = rfid_reader.MFRC522_Anticoll()
                if status == rfid_reader.MI_OK:
                    uid = "".join([str(x) for x in raw_uid])
                    num = len(uid)
                    print(f"RFID card detected: UID={uid}, NUM={num}")
                    call_rfid_reading(str(uid), str(num))

        except Exception as e:
            client.publish("response/rfid", json.dumps({"error": str(e)}))
            print(f"Error during RFID read: {e}")

        time.sleep(1)


def on_connect(client, userdata, flags, rc):
    # topics
    print(f"Connected to MQTT broker with result code {rc}")
    client.subscribe("command/rfid")
    client.subscribe("command/weather")


def on_message(client, userdata, msg):
    global rfid_listening
    topic = msg.topic
    payload = json.loads(msg.payload.decode())
    print(f"Received message on topic {topic}: {payload}")

    if topic == "command/rfid":
        # card handler
        if payload.get("action") == "start_rfid":
            print("Starting RFID listener...")
            if not rfid_listening:
                rfid_listening = True
                threading.Thread(target=rfid_listener, daemon=True).start()

        elif payload.get("action") == "stop_rfid":
            print("Stopping RFID listener...")
            rfid_listening = False

    # weahter handler
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
