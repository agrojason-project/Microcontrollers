class SensorData:
    def __init__(self, timestamp, temperature_in, temperature_out, humidity_in, humidity_out, light, pH, humidity_substrate):
        self.timestamp = timestamp
        self.temperature_in = temperature_in
        self.temperature_out = temperature_out
        self.humidity_in = humidity_in
        self.humidity_out = humidity_out
        self.light = light
        self.pH = pH
        self.humidity_substrate = humidity_substrate