from Sensor import Sensor
from Point import Point
class Target():
	def __init__(self, localization):
		self.localization = localization #type: Point
		self.covering_sensors=[] #type: list[Sensor]


	def get_key(self):
		return self.localization

	def __hash__(self) -> int:
		return self.get_key().__hash__()

	def __eq__(self, obj) -> bool:
		if obj==None:
			return False
		return obj.localization==self.localization

