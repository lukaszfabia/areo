import asyncio
import json
from typing import Optional

from paho.mqtt.client import Client as MQTTClient
from app.main import logger
from app.db.models.weather import Weather


class RaspberryPiService:
    broker = "10.108.33.124"
    port = 1883

    # ./raspberry/sender.py
    def __init__(self, broker: str = broker, port: int = port):
        self.client = MQTTClient()
        self.client.on_message = self._on_message
        self.client.on_connect = self._on_connect
        self.loop = asyncio.get_event_loop()
        self.response_data = None

        self.client.connect(broker, port, 60)
        self.client.loop_start()

    def _on_connect(self, client, userdata, flags, rc):
        print(f"Connected to MQTT broker with result code {rc}")
        client.subscribe("response/weather")
        client.subscribe("response/rfid")

    def _on_message(self, client, userdata, msg):
        print(f"Received message on topic {msg.topic}: {msg.payload.decode()}")
        self.response_data = json.loads(msg.payload)

    async def send_command(self, topic: str, message: dict, timeout: int = 10):
        """Send what u want to raspberry pi

        Usage:
            wrap in try catch block
            response = await raspberry_service.send_command(
                                topic="command/weather", # your topic alternative command/rfid
                                message={"action": "get_weather"}, # action = start_rfid for starting listening on card
                                timeout=5
                        )
        """
        self.response_data = None
        self.client.publish(topic, json.dumps(message))

        try:
            await asyncio.wait_for(self._wait_for_response(), timeout=timeout)
            return self.response_data
        except asyncio.TimeoutError:
            print(f"Timeout: No response from Raspberry Pi for topic {topic}")
            return None

    async def _wait_for_response(self):
        while self.response_data is None:
            await asyncio.sleep(0.1)

    async def get_weather(self, reader: str) -> Optional[Weather]:
        """Please provide emaila as a reader"""

        try:
            response = await self.send_command(
                topic="command/weather",
                message={"action": "get_weather"},
                timeout=20,
            )
        except:
            return None

        weather = Weather(
            temperature=response["temperature"],
            altitude=response["altitude"],
            pressure=response["pressure"],
            humidity=response["humidity"],
            reader=reader,
        )

        return weather

    async def read_rfid(self) -> Optional[str]:
        try:
            result = await self.send_command(
                topic="command/rfid",
                message={"action": "start_rfid"},
                timeout=30,
            )
            if not result or "uid" not in result:
                print("RFID read failed: Invalid response")
                return None
        except TimeoutError:
            print("RFID read timeout")
            return None

        uid = result["uid"]

        try:
            await self.send_command(
                topic="command/rfid",
                message={"action": "stop_rfid"},
                timeout=30,
            )
        except TimeoutError:
            print("Failed to stop RFID reading")

        return uid
