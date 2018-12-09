import time


class Statistic:
    def __init__(self,targets:list,sensors:list):
        self.start_time=time.time()
        self.targets_number=len(targets)
        self.sensors=sensors


    def get_simulation_time(self):
        """
        zwraca czas symulacji
        :return:
        """
        return round(self.stop-self.start_time,2)
    def stop_time(self):
        """
        zapisuje czas końca symulacji
        """
        self.stop=time.time()


    def get_percent_observed_targets(self):
        """
        zwraca procent obserwowanych celów
        :return:
        """
        targets_set=set()
        for sensor in self.sensors:
            if(sensor.active==True):
                targets_set.update(sensor.covering_targets)
        return round(100*(len(targets_set)/self.targets_number),2) #type: int








