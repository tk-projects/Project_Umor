import time
import board
import busio
import adafruit_ads1x15.ads1115 as ads
from adafruit_ads1x15.analog_in import AnalogIn


i2c = busio.I2C(board.SCL, board.SDA)
adc = ads.ADS1115(i2c)


class humidity_sensor:
    def __init__(self, sensor_id, adc_channel, unit = None, ):
        self.sensor_id = sensor_id
        self.unit = "% air moisture"
        print('adc, ads.P' + str(adc_channel))
        #self.adc_channel = AnalogIn(adc, ads.P0)
        self.adc_channel = AnalogIn(adc, getattr(ads, 'P' + str(adc_channel)))
        #self.adc_channel = AnalogIn(eval('adc, ads.P' + str(adc_channel)))
        self.sensor_data = []

    def read(self):
        print (self.adc_channel.value, self.adc_channel.voltage)
        time.sleep