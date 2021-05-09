import pandas as pd
import seaborn as sns

class Equipment:
    vendor = "unknown"
    sensors = []
    def __init__(self, name):
        self.name = name

    def add_sensor(sensor):
        sensors.append(sensor)

class Sensor:
    units = "unknown"
    data = pd.DataFrame()
    def __init__(self, name):
        self.name = name

    def load_data(self, csvPath):
        self.data = pd.read_csv(csvPath, header = None, delimiter = ";")
        self.data.columns = ["timestamp","value"]
        self.data.name = csvPath[0:name_csv_files[i].index(".")]

    def visualize(self, graph):
        graph.
        pass

    def calculate_aggregate(calculation_name, aggregate_name, parameter):
        pass

a = Equipment("zarizeni 1")
b = Equipment("zarizeni 2")

b.vendor = "aaa"
print(a.name)
print(a.vendor)

print(b.name)
print(b.vendor)

s = Sensor("sen")
s.