import time
import board
import busio
import adafruit_ads1x15.ads1115 as ads
from adafruit_ads1x15.analog_in import AnalogIn


i2c = busio.I2C(board.SCL, board.SDA)
adc = ads.ADS1115(i2c)

class humidity_sensor:
    def __init__(self, sensor_id, adc_channel, name, sensor_group_id, sensor_cluster_id, unit = None, max_calibration_value = 0, min_calibration_value = 0):
        self.sensor_id = sensor_id
        self.name = name
        self.unit = unit
        self.sensor_cluster = sensor_cluster_id;
        self.adc_channel_idx = adc_channel
        self.adc_channel = AnalogIn(adc, getattr(ads, 'P' + str(self.adc_channel_idx)))
        self.sensor_group = sensor_group_id;
        self.sensor_data = [];
        self.max_calibration_value = max_calibration_value;
        self.min_calibration_value = min_calibration_value;

    def read(self):
        #print (self.adc_channel.value, self.adc_channel.voltage)
        humidity = abs(round(-1*(self.adc_channel.value-self.max_calibration_value)/(self.max_calibration_value - self.min_calibration_value), 2)*100)
        print("\n",humidity, self.unit)
        time.sleep(0.4)
        return humidity

    def calibrate(self):
        print("________________________________________________________________________________________________________")
        print("________________________________________________________________________________________________________\n")
        print("Verbinde mit Sensor.")
        dauer = 32
        for _ in range(dauer):
            print(".", end="", flush=True)
            time.sleep(0.04)
        
        print("\n\nSensor bereit für Kalibrierung.")
        time.sleep(1)
        sensor_is_dry = input("\nWenn der Sensor trocken ist mit Enter bestätigen (andere Taste zum abbrechen)")
    

        if sensor_is_dry =="":
            max_calibration_value = self.adc_channel.value;

            print("\n\nMesswerte von Sensor ", self.sensor_id, " bei Trockenheit:")
            print("__________________________________________")

            for i in range(0,10):
                if self.adc_channel.value > max_calibration_value:
                    max_calibration_value = self.adc_channel.value;
                print("Wert",i+1,":\t",self.adc_channel.value)
                time.sleep(0.4)
        else:
            print("\nKalibrierung abgebrochen")
            return

        time.sleep(1)

        sensor_is_humid = input("\nJetzt den Sensor ins Wasser stellen und mit Enter bestätigen (andere Taste zum abbrechen)")

        if sensor_is_humid =="":
            min_calibration_value = self.adc_channel.value;

            print("\n\nMesswerte von Sensor", self.sensor_id, " bei Feuchtigkeit:")
            print("__________________________________________")

            for i in range(0,10):
                if self.adc_channel.value < min_calibration_value:
                    min_calibration_value = self.adc_channel.value;
                print("Wert ",i+1,":\t",self.adc_channel.value)
                time.sleep(0.4)
        else:
            print("\nKalibrierung abgebrochen")
            return
        
        self.min_calibration_value = min_calibration_value;
        self.max_calibration_value = max_calibration_value;

        print("______________________________________________________________________________")
        print("\nDie Sensor-calibration_values wurden wie folgt kalibriert:\n\n   Bei absoluter Trockenheit:\t", self.max_calibration_value)
        print("\n   Bei absoluter Feuchtigkeit:\t", self.min_calibration_value)
        print("______________________________________________________________________________")

    def to_dict(self):
        return {
            "sensor_id": self.sensor_id,
            "name": self.name,
            "adc_channel": self.adc_channel_idx,
            "unit": self.unit,
            "min_calibration_value": self.min_calibration_value,
            "max_calibration_value": self.max_calibration_value,
            "sensor_group_id":self.sensor_group_id,
            "sensor_cluster_id":self.sensor_cluster_id,
        }  