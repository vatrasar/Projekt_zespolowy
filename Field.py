from Target import Target

class Field:

    def __init__(self,target=None):
        self.targets = []
        if target==None:
            self.sensors=[] #type: list
        else:
            self.sensors=target.covering_sensors #type: list
            self.targets.append(target) #type: list.
            for sensor in self.sensors:
                sensor.fields.append(self)

    def __eq__(self, o) -> bool:
        return o.targets==self.targets and o.sensors==self.sensors

    def get_key(self):
        return (tuple(self.targets),tuple(self.sensors))
    def __hash__(self) -> int:
         return self.get_key().__hash__()










