from graph import Node
class Sensor(Node):

	def __init__(self,battery,sensing_range,localization):
		"""
		:param battery: poziom naładowania baterii (0 jeśli jest rozładowana)
		:param sensing_range:typ Point
		:param localization: tylko przy rozwiązaniu dystrybucyjnym(zachłannynm)
		:param active: true gdy sensor aktywny,false gdy nieaktywny
		:param covering_targets: lista targetów które są pokryte przez dany sensor
		"""
		super().__init__(0, 0)
		self.battery = battery
		self.sensing_range = sensing_range
		self.localization = localization
		self.active = True
		self.covering_targets = []
	def set_sensor_state(self,new_state:bool):
		self.active=new_state

	def get_key(self):
		return (self.active,self.localization,super().get_key())

	def __eq__(self, o) -> bool:
		return self.localization==o.localizatio and self.active==o.active and super().__eq__()

	def __hash__(self) -> int:
		return hash(self.get_key())








