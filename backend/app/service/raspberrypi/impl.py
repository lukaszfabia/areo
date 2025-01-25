from app.service.raspberrypi.serivce import RaspberryPiService
from tests.config import *
from app.db.models import weather
import adafruit_bme280.advanced as adafruit_bme280
import w1thermsensor
import neopixel
import board
import busio

HIGH_TEMPERATURE = 30.0
LOW_TEMPERATURE = 5.0

HIGH_ALTITUDE = 100
LOW_ALTITUDE = 0.0

HIGH_PRESSURE = 1030.0
LOW_PRESSURE = 1000.0

HIGH_HUMIDITY = 75.0 # in %
LOW_HUMIDITY = 0.0 # in %

class RaspberryPiServiceImpl(RaspberryPiService): 
    def __init__(self):
        self.__SensorHandler = SensorHandler()
        self.__LedController = LedController()
   
    def __buzzer(self, state):
        GPIO.output(buzzerPin, not state)

    def get_weather(self):
        """Get weather stats"""

        self.__buzzer(True)

        temperature = self.__SensorHandler.temperature
        altitude = self.__SensorHandler.altitude
        pressure = self.__SensorHandler.pressure
        humidity = self.__SensorHandler.humidity
        reader = ""

        self.__buzzer(False)

        self.__LedController.visualize_with_leds(temperature=temperature, altitude=altitude,
                                                 pressure=pressure, humidity=humidity)

        return weather(temperature=temperature, altitude=altitude, 
                       pressure=pressure, humidity=humidity, reader=reader)

class Color:
        black = (0, 0, 0)
        white = (255, 255, 255)
        red = (255, 0, 0)
        lime = (0, 255, 0)
        blue = (0, 0, 255)
        yellow = (255, 255, 0)
        cyan = (0, 255, 255)
        magenta = (255, 0, 255)
        silver = (192, 192, 192)
        grey = (128, 128, 128)
        maroon = (128, 0, 0)
        olive = (128, 128, 0)
        green = (0, 128, 0)
        purple = (128, 0, 128)
        teal = (0, 128, 128)
        navy = (0, 0, 128)
        orange = (255, 128, 0)

class LedController:
    class InnerColor:
        def __init__(self, r, g, b, brightness):
            self.r = r
            self.g = g
            self.b = b
            self.brightness = brightness

        @classmethod
        def black(cls):
            return cls(*Color.black, 1)

        @property
        def color(self):
            return int(self.r * self.brightness), int(self.g * self.brightness), int(self.b * self.brightness)

        @color.setter
        def color(self, color_tuple):
            self.r, self.g, self.b = color_tuple

    def __init__(self, brightness=1.0 / 32, auto_write=False):
        self.__pixels = neopixel.NeoPixel(board.D18, 8, brightness=brightness, auto_write=auto_write)
        self.__colors = [self.InnerColor.black() for _ in range(8)]
        self.update_all()

    def update_all(self):
        for inx in range(len(self.__colors)):
            self.__pixels[inx] = self.__colors[inx].color
        self.__pixels.show()

    def rainbow(self):
        self.__colors[0].color = Color.red
        self.__colors[1].color = Color.orange
        self.__colors[2].color = Color.yellow
        self.__colors[3].color = Color.lime
        self.__colors[4].color = Color.green
        self.__colors[5].color = Color.cyan
        self.__colors[6].color = Color.blue
        self.__colors[7].color = Color.purple
        self.update_all()

    def visualize_with_leds(self, temperature, altitude, pressure, humidity):

        # 2 LEDs for temperature
        if temperature > HIGH_TEMPERATURE:
            self.__colors[0].color = Color.red
            self.__colors[1].color = Color.red
        elif temperature > LOW_TEMPERATURE:
            self.__colors[0].color = Color.green
            self.__colors[1].color = Color.green
        else:
            self.__colors[0].color = Color.blue
            self.__colors[1].color = Color.blue

        # 2 LEDs for altitude
        if altitude > HIGH_ALTITUDE:
            self.__colors[2].color = Color.red
            self.__colors[3].color = Color.red
        elif altitude > LOW_ALTITUDE:
            self.__colors[2].color = Color.green
            self.__colors[3].color = Color.green
        else:
            self.__colors[2].color = Color.blue
            self.__colors[3].color = Color.blue

        # 2 LEDs for pressure            
        if pressure > HIGH_PRESSURE:
            self.__colors[4].color = Color.red
            self.__colors[5].color = Color.red
        elif pressure > LOW_PRESSURE:
            self.__colors[4].color = Color.green
            self.__colors[5].color = Color.green
        else:
            self.__colors[4].color = Color.blue
            self.__colors[5].color = Color.blue

        # 2 LEDs for humidity
        if humidity > HIGH_HUMIDITY:
            self.__colors[6].color = Color.red
            self.__colors[7].color = Color.red
        elif humidity > LOW_HUMIDITY:
            self.__colors[6].color = Color.green
            self.__colors[7].color = Color.green
        else:
            self.__colors[6].color = Color.blue
            self.__colors[7].color = Color.blue


class SensorHandler:
    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.__sensor = adafruit_bme280.Adafruit_BME280_I2C(i2c, 0x76)
        self.__init_sens()
        self.__thermometer = w1thermsensor.W1ThermSensor()

    def __init_sens(self):
        self.__sensor.sea_level_preasure = 1013.25
        self.__sensor.standby_period = adafruit_bme280.STANDBY_TC_500
        self.__sensor.iir_filter = adafruit_bme280.IIR_FILTER_X16
        self.__sensor.overscan_pressure = adafruit_bme280.OVERSCAN_X16
        self.__sensor.overscan_humidity = adafruit_bme280.OVERSCAN_X1
        self.__sensor.overscan_temperature = adafruit_bme280.OVERSCAN_X2

    @property
    def temperature(self):
        return self.__thermometer.get_temperature()
    
    @property
    def altitude(self):
        return self.__sensor.altitude
    
    @property
    def pressure(self):
        return self.__sensor.pressure
    
    @property
    def humidity(self):
        return self.__sensor.humidity