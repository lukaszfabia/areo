from PIL import Image, ImageDraw, ImageFont

# dodac tests.config
from tests.config import *
import adafruit_bme280.advanced as adafruit_bme280
import lib.oled.SSD1331 as SSD1331
import RPi.GPIO as GPIO
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

HIGH_HUMIDITY = 75.0  # in %
LOW_HUMIDITY = 0.0  # in %
buzzerPin = 18


class WeatherHandler:
    def __init__(self):
        self.__LedController = LedController()
        self.__ExerciseHandler = ExerciseHandler()
        self.__ExerciseHandler.first_print_all()

    def __buzzer(self, state):
        GPIO.output(buzzerPin, not state)

    def get_weather(self, reader: str):
        """Get weather stats"""

        self.__buzzer(True)

        temperature = self.__ExerciseHandler.SensorHandler.temperature
        altitude = self.__ExerciseHandler.SensorHandler.altitude
        pressure = self.__ExerciseHandler.SensorHandler.pressure
        humidity = self.__ExerciseHandler.SensorHandler.humidity

        self.__buzzer(False)

        self.__LedController.visualize_with_leds(
            temperature=temperature,
            altitude=altitude,
            pressure=pressure,
            humidity=humidity,
        )
        self.__ExerciseHandler.print_all()

        return {
            "temperature": temperature,
            "altitude": altitude,
            "pressure": pressure,
            "humidity": humidity,
            "reader": reader,
        }


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
            return (
                int(self.r * self.brightness),
                int(self.g * self.brightness),
                int(self.b * self.brightness),
            )

        @color.setter
        def color(self, color_tuple):
            self.r, self.g, self.b = color_tuple

    def __init__(self, brightness=1.0 / 32, auto_write=False):
        self.__pixels = neopixel.NeoPixel(
            board.D18, 8, brightness=brightness, auto_write=auto_write
        )
        self.__colors = [self.InnerColor.black() for _ in range(8)]
        self.update_all()

    def update_all(self):
        for inx in range(len(self.__colors)):
            self.__pixels[inx] = self.__colors[inx].color
        self.__pixels.show()

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


class Font:
    ARIAL = ImageFont.truetype("fonts/arial.ttf")
    TIMES = ImageFont.truetype("fonts/times.ttf")
    MATORAN = ImageFont.truetype("fonts/Matoran.ttf")


class OledHandler:
    # Modes
    RGB = "RGB"
    RGBA = "RGBA"
    CMYK = "CMYK"

    GRAY = (40, 40, 40)

    def __init__(self, background_color, background_file):
        self.__display = SSD1331.SSD1331()
        self.__display.Init()
        self.__display.clear()
        self.__background = Image.open(background_file)
        self.__printer = ImageDraw.Draw(self.__background)
        self.__background_color = background_color

    def show(self):
        self.__display.ShowImage(self.__background)

    def clear(self):
        self.__display.clear()

    def reset(self):
        self.__display.reset()

    @property
    def width(self):
        return self.__display.width

    @property
    def height(self):
        return self.__display.height

    def base_print(self, xy, text, color=None, font=Font.ARIAL):
        self.__printer.text(xy, text, fill=color, font=font)

    def base_clear(self, xy):
        self.__printer.rectangle(xy, fill=self.__background_color)


class ExerciseHandler:
    TEMPERATURE_DELTA = 0.1
    HUMIDITY_DELTA = 0.1
    ALTITUDE_DELTA = 0.1
    PRESSURE_DELTA = 1
    PIXEL_RIGHT = 30
    MAX_RIGHT = 96

    def __init__(self):
        self.oled_handler = OledHandler(
            OledHandler.GRAY, "app/service/raspberrytpi/images/background.png"
        )
        self.sensorHandler = SensorHandler()
        self.all_handlers = [
            self.SensorPrintHandler(
                self.oled_handler,
                self.sensorHandler.temperature,
                (self.PIXEL_RIGHT, 3),
                ((self.PIXEL_RIGHT, 0), (self.MAX_RIGHT, 20)),
                self.TEMPERATURE_DELTA,
                "Temp:",
                "C",
            ),
            self.SensorPrintHandler(
                self.oled_handler,
                self.sensorHandler.humidity,
                (self.PIXEL_RIGHT, 19),
                ((self.PIXEL_RIGHT, 15), (self.MAX_RIGHT, 35)),
                self.HUMIDITY_DELTA,
                "Hum:",
                "%",
            ),
            self.SensorPrintHandler(
                self.oled_handler,
                self.sensorHandler.altitude,
                (self.PIXEL_RIGHT, 35),
                ((self.PIXEL_RIGHT, 30), (self.MAX_RIGHT, 50)),
                self.ALTITUDE_DELTA,
                "Alt:",
                "m",
            ),
            self.SensorPrintHandler(
                self.oled_handler,
                self.sensorHandler.pressure,
                (self.PIXEL_RIGHT, 50),
                ((self.PIXEL_RIGHT, 45), (self.MAX_RIGHT, 65)),
                self.PRESSURE_DELTA,
                "Press:",
                "hPa",
            ),
        ]

    class SensorPrintHandler:
        def __init__(
            self,
            oled_handler,
            accessor,
            pixel_tuple,
            clear_tuple,
            value_delta,
            extra_text,
            si_unit,
        ):
            self.oled_handler = oled_handler
            self.current_value = accessor()
            self.value_delta = value_delta
            self.accessor = accessor
            self.print_tuple = pixel_tuple
            self.clear_tuple_of_tuples = clear_tuple
            self.extra_text = extra_text
            self.si_unit = si_unit

        def conditioned_print(self, font=Font.ARIAL, color=None):
            new_value = self.accessor()
            if abs(self.current_value - new_value) > self.value_delta:
                self.current_value = new_value
                self.print(font, color)

        def print(self, font=Font.ARIAL, color=None):
            self.clearer()
            text = f"{self.extra_text} {round(self.current_value, 1)} {self.si_unit}"
            self.oled_handler.base_print(self.print_tuple, text, color=color, font=font)

        def clearer(self):
            self.oled_handler.base_clear(self.clear_tuple_of_tuples)

    def first_print_all(self):
        for handler in self.all_handlers:
            handler.print()
        self.oled_handler.show()

    def print_all(self):
        for handler in self.all_handlers:
            handler.conditioned_print()
        self.oled_handler.show()
