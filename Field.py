from Target import Target

class Field:

    def __init__(self,target=None):
        self.targets = []
        if target==None:
            self.sensors=[] #type: list
        else:
            self.sensors=target.covering_sensors #type: list
            self.targets.append(target) #type: list







