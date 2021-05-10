import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 150

DATA_FOLDER = os.getcwd() + "/data/"


class Equipment:
    """
    Represents generic equipment with basic attributes

    Attributes
    ----------
    name: str
        TBD
    vendor: str
        TBD
    sensors: list (of Sensor)
        TDB
    """
    
    def __init__(self, name, vendor = "unknown"):
        self.name = name
        self.sensors = []
        self.vendor = vendor

    def __str__(self):
        return self.name

    def add_sensor(self, sensor):
        self.sensors.append(sensor)

    def visualize_all_sensors(self):
        fig = plt.figure()
        for sensor in self.sensors:
            plt.plot_date(sensor.data[Sensor._timestamp_column_name], sensor.data[Sensor._value_column_name], '-', label=sensor.name, linewidth=1)
        plt.legend()
        plt.show()

class Sensor:
    _timestamp_column_name = "timestamp"
    _value_column_name = "value"
    def __init__(self, name, units = "unknown"):
        self.name = name
        self.units = units
        self.data = pd.DataFrame()

    def __str__(self):
        return self.name

    def load_data(self, csvPath):
        headers = [Sensor._timestamp_column_name,Sensor._value_column_name]
        self.data = pd.read_csv(csvPath, header = None, delimiter = ";", names = headers, parse_dates=[Sensor._timestamp_column_name])
        self.data.name = csvPath[0:csvPath.index(".")]

    def visualize(self):
        self.data.plot(x=_timestamp_column_name, y=_value_column_name, linewidth=1)
        plt.xticks(rotation=20)
        plt.show()
        pass
    
    def show_statistics(self):
        print(self.data.describe(datetime_is_numeric=True, include='all'))

class AggregatedSensor(Sensor):
    def calculate_aggregate(calculation_name, aggregate_name, time_window_size_in_seconds):
        pass

    def visualize_all_aggregates(self):
        pass

class AlarmSensor(Sensor):
    pass

oven1 = Equipment("Baking Oven 1")
oven2 = Equipment("Baking Oven 2")
  
s1 = Sensor("Temperature")
s1.load_data(DATA_FOLDER + "Zarizeni1_SensorTeplota.csv")

s2 = Sensor("Pressure")
s2.load_data(DATA_FOLDER + "Zarizeni1_SensorTlak.csv")

s3 = Sensor("Temperature")
s3.load_data(DATA_FOLDER + "Zarizeni2_SensorTeplota.csv")

s4 = Sensor("Pressure")
s4.load_data(DATA_FOLDER + "Zarizeni2_SensorTlak.csv")

oven1.add_sensor(s1)
oven1.add_sensor(s2)
oven2.add_sensor(s3)
oven2.add_sensor(s4)

for s in oven1.sensors:
    print(s)
    s.show_statistics()
    print(s.data.describe(datetime_is_numeric=True, include='all'))

#oven1.visualize_all_sensors()

print("data shown")

""" s1.visualize(None)
s2.visualize(None)
s3.visualize(None)
s4.visualize(None)
 """

equipment = {}
def load_all_files_to_equipments_and_sensors():
    csv_files = [f for f in os.listdir(DATA_FOLDER) if f.endswith(".csv")]
    for csv_file in csv_files:
        equipment_name = csv_file[0:csv_file.index("_")]
        sensor_name = csv_file[csv_file.index("_")+1:csv_file.index(".")]
        sensor = Sensor(sensor_name)
        sensor.load_data(DATA_FOLDER + csv_file)
        if equipment_name not in equipment:
            equipment[equipment_name] = Equipment(equipment_name)
        equipment[equipment_name].add_sensor(sensor)
load_all_files_to_equipments_and_sensors()    
