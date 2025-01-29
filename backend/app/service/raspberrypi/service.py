import asyncio
import json
from typing import Optional

from paho.mqtt.client import Client as MQTTClient
from app.main import logger
from app.db.models.weather import Weather


class RaspberryPiService:
    broker = "10.108.33.xxx"
    port = 1883

    # ./raspberry/sender.py
    def __init__(self, broker: str = broker, port: int = port):
        self.client = MQTTClient()
        self.client.on_message = self.__on_message
        self.client.on_connect = self.__on_connect
        self.loop = asyncio.get_event_loop()
        self.response_data = None

        self.client.connect(broker, port, 60)
        self.client.loop_start()

    def __on_connect(self, client, userdata, flags, rc):
        logger.info(f"Connected to MQTT broker with result code {rc}")
        client.subscribe("response/weather")
        client.subscribe("response/rfid")

    def __on_message(self, client, userdata, msg):
        logger.info(f"Received message on topic {msg.topic}: {msg.payload.decode()}")
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

        for _ in range(timeout * 10):
            if self.response_data is not None:
                return self.response_data
            await asyncio.sleep(0.1)

        raise TimeoutError("No response from Raspberry Pi")

    async def get_weather(self, reader: str) -> Optional[Weather]:
        """Please provide emaila as a reader"""

        try:
            response = await self.send_command(
                topic="command/weather",
                message={"action": "get_weather"},
                timeout=10,
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
        except TimeoutError:
            return None

        uid = result["uid"]

        try:
            await self.send_command(
                topic="command/rfid",
                message={"action": "stop_rifd"},
                timeout=10,
            )
        except TimeoutError:
            logger.error("Failed to stop listening on rfid")

        return uid
