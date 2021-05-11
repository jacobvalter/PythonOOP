import os
import pandas as pd
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
        return f"{self.name} with {len(self.sensors)} sensors aa " 

    def __repr__(self):
        return f"{self.name} with {len(self.sensors)} sensors"

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
        headers = [Sensor._timestamp_column_name, Sensor._value_column_name]
        self.data = pd.read_csv(csvPath, header = None, delimiter = ";", names = headers, parse_dates=[Sensor._timestamp_column_name])
        self.data.name = csvPath[0:csvPath.index(".")]
        self.data.set_index(Sensor._timestamp_column_name)

    def visualize(self):
        self.data.plot(x = Sensor._timestamp_column_name, y = Sensor._value_column_name, linewidth=1)
        plt.xticks(rotation=20)
        plt.show()
        pass
    
    def show_statistics(self):
        print(self.data.describe(datetime_is_numeric=True, include='all'))

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
        """
        aggregate_data = pd.DataFrame(columns=(Sensor._timestamp_column_name, Sensor._value_column_name)
        aggregate_data.name = aggregate_name
        aggregate_data.set_index(Sensor._timestamp_column_name)
        """
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

class AlarmSensor(Sensor):
    pass

""" oven1 = Equipment("Baking Oven 1")
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
    print(s.data.describe(datetime_is_numeric=True, include='all')) """

aggregated_sensor = AggregatedSensor("Temperature")
aggregated_sensor.load_data(DATA_FOLDER + "Zarizeni1_SensorTeplota.csv")
aggregated_sensor.visualize()
aggregated_sensor.calculate_aggregate("as", AggregatedSensor._aggr_average, 1800)
aggregated_sensor.visualize_specific_aggregate("as")

#oven1.visualize_all_sensors()

print("data shown")

""" s1.visualize(None)
s2.visualize(None)
s3.visualize(None)
s4.visualize(None)
 """


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
print(equipment)  
print(equipment['Zarizeni1']) """