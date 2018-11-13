class Scheduler:

    def __init__(self,sensors_list,sensing_range):
        """

        :param sensors_list:lista obiektów typu Sensor
        :param sensing_range:
        :param targets_list:pytanie czy będziemy obserwować cele czy jakiś obszar
        jeśli obszar to parametr jest niepotrzebny
        """
        self.sensor_list=sensors_list
        self.sensor_range=sensing_range
    def get_sensor_list(self):
        pass
