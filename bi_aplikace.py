# Authors: Jakub Lenk, Jana Koukalova

import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 150

DATA_FOLDER = os.getcwd() + "/data/"

class Sensor:
    _timestamp_column_name = "timestamp"
    _value_column_name = "value"
    def __init__(self, name, units = "unknown"):
        self.name = name
        self.units = units
        self.data = pd.DataFrame()

    def load_data(self, csvPath):
        headers = [Sensor._timestamp_column_name, Sensor._value_column_name]
        self.data = pd.read_csv(csvPath, header = None, delimiter = ";", names = headers, parse_dates=[Sensor._timestamp_column_name])
        self.data.name = csvPath[0:csvPath.index(".")]
        self.data.set_index(Sensor._timestamp_column_name)

    def visualize(self):
        self.data.plot(x = Sensor._timestamp_column_name, y = Sensor._value_column_name, linewidth=1)
        plt.xticks(rotation=20)
        plt.show()
        
    def show_statistics(self):
        print(self.data.describe(datetime_is_numeric=True, include='all'))

class Equipment:
    def __init__(self, name, vendor = "unknown"):
        self.name = name
        self.sensors = []
        self.vendor = vendor
    
    def __str__(self):
        return f"{self.name} with {len(self.sensors)} sensors" 
    
    def __repr__(self):
        return f"{self.name} / {len(self.sensors)}"

    def add_sensor(self, sensor):
        self.sensors.append(sensor)

    def visualize_all_sensors(self):
        fig = plt.figure()
        for sensor in self.sensors:
            plt.plot_date(sensor.data[Sensor._timestamp_column_name], sensor.data[Sensor._value_column_name], '-', label=sensor.name, linewidth=1)
        plt.legend()
        plt.show()

class AggregatedSensor(Sensor):
    _aggr_average = "AVG"
    _aggr_minimum = "MIN"
    _aggr_maximum = "MAX"
    _valid_aggregates = [_aggr_average, _aggr_minimum, _aggr_maximum]

    def __init__(self, name, units = "unknown"):
        super().__init__(name, units)
        self.aggregated_data = {}
    
    def calculate_aggregate(self, calculation_name, aggregate_name, time_window_size_in_seconds):
        if (aggregate_name not in AggregatedSensor._valid_aggregates):
            print(f"aggregate {aggregate_name} is not valid")
            return
        time_window_edges = []
        aggregate_data = []

        start_time = self.data[Sensor._timestamp_column_name].min()
        end_time = self.data[Sensor._timestamp_column_name].max()
        current_time = start_time
        while current_time < end_time:
            time_window_edges.append(current_time)
            current_time = current_time + pd.Timedelta(seconds=time_window_size_in_seconds)

        for i in range(len(time_window_edges)-1):
            mask = (self.data[Sensor._timestamp_column_name]>=time_window_edges[i]) & (self.data[Sensor._timestamp_column_name]<time_window_edges[i+1])
            aggregate_value = 0
            if (aggregate_name == AggregatedSensor._aggr_average):
                aggregate_value = self.data[mask][Sensor._value_column_name].mean()
            elif (aggregate_name == AggregatedSensor._aggr_minimum):
                aggregate_value = self.data[mask][Sensor._value_column_name].min()
            elif (aggregate_name == AggregatedSensor._aggr_maximum):
                aggregate_value = self.data[mask][Sensor._value_column_name].max()
            aggregate_sample = {Sensor._timestamp_column_name: time_window_edges[i], Sensor._value_column_name: aggregate_value}
            aggregate_data.append(aggregate_sample)
        
        aggregate_df = pd.DataFrame(aggregate_data)
        aggregate_df.name = calculation_name
        aggregate_df.set_index(Sensor._timestamp_column_name)
        self.aggregated_data[calculation_name] = aggregate_df
        
    def visualize_all_aggregates(self):
        pass

    def visualize_specific_aggregate(self, name):
        if (name not in self.aggregated_data):
            print(f"aggregate with name {name} has not been created")
            return 
        self.aggregated_data[name].plot(x=Sensor._timestamp_column_name, y=Sensor._value_column_name, linewidth=1)
        plt.xticks(rotation=20)
        plt.show()
        pass

""" s1 = Sensor("Teplota", "C")
s1.load_data(DATA_FOLDER + "Zarizeni1_SensorTeplota.csv")
#s1.visualize()

s2 = Sensor("Tlak", "bar")
s2.load_data(DATA_FOLDER + "Zarizeni1_SensorTlak.csv")
#s2.visualize()

eq1 = Equipment("Vypekaci pec 1")
eq1.add_sensor(s1)
eq1.add_sensor(s2)
eq1.visualize_all_sensors() """

ags = AggregatedSensor("teplota")
ags.load_data(DATA_FOLDER + "Zarizeni1_SensorTeplota.csv")
ags.visualize()
ags.calculate_aggregate("as", AggregatedSensor._aggr_average, 1800)
ags.visualize_specific_aggregate("as")


""" equipment = {}
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
#equipment["Zarizeni2"].visualize_all_sensors()
#print(equipment["Zarizeni2"])
print(equipment) """