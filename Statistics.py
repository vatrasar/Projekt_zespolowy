import time


class Statistic:
    def __init__(self,targets:list,sensors:list):
        self.start_time=time.time()
        self.targets=targets
        self.sensors=sensors

    def get_simulation_time(self):
        return round(time.time()-self.start_time,2)

    def update_state(self,sensors):
        self.sensors=sensors

    def get_active_sensors_number(self):
        return len(list(filter(lambda x:x.active,self.sensors)))

    def get_charged_sensors_count(self):
        return len(list(filter(lambda x:x.battery>0,self.sensors)))

    def get_percent_observed_targets(self):
        targets_set=set()
        for sensor in self.sensors:
            if(sensor.active==True):
                targets_set.update(sensor.covering_targets)
        return round(100*(len(targets_set)/len(self.targets)),2) #type: int








