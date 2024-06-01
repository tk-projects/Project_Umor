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
        self.sensor_data = [];
        self.max_offset = 0;
        self.min_offset = 0;

    def read(self):
        print (self.adc_channel.value, self.adc_channel.voltage)
        time.sleep

    def calibrate(self):
        sensor_is_dry = input("\nWenn der Sensor trocken ist mit Enter bestätigen (andere Taste zum abbrechen)")
    

        if sensor_is_dry =="":
            max_offset = self.adc_channel.value;

            print("\nMesswerte von Sensor", self.sensor_id, ":")
            print("_______________________")

            for i in range(0,10):
                if self.adc_channel.value > max_offset:
                    max_offset = self.adc_channel.value;
                print("Wert ",i,": ",self.adc_channel.value)
                time.sleep(0.4)
        else:
            print("\nKalibrierung abgebrochen")
            return

        time.sleep(1)

        sensor_is_humid = input("\nJetzt den Sensor ins Wasser stellen und mit Enter bestätigen (andere Taste zum abbrechen)")

        if sensor_is_humid =="":
            min_offset = self.adc_channel.value;

            print("\nMesswerte von Sensor", self.sensor_id, ":")
            print("_______________________")

            for i in range(0,10):
                if self.adc_channel.value < min_offset:
                    min_offset = self.adc_channel.value;
                print("Wert ",i,": ",self.adc_channel.value)
                time.sleep(0.4)
        else:
            print("\nKalibrierung abgebrochen")
            return
        
        self.min_offset = min_offset;
        self.max_offset = max_offset;

        print("_______________________________________________________________________________________________")
        print("\nDie Sensor-Offsets wurden wie folgt kalibriert:\n\n   Bei absoluter Trockenheit: ", self.max_offset)
        print("\n   Bei absoluter Feuchtigkeit: ", self.min_offset)
        print("_______________________________________________________________________________________________")



    