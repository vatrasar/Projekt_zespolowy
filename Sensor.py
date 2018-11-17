class Sensor:

	def __init__(self,battery,sensing_range,localization):
		"""
		:param battery: poziom naładowania baterii (0 jeśli jest rozładowana)
		:param sensing_range:typ Point
		:param localization: tylko przy rozwiązaniu dystrybucyjnym(zachłannynm)
		:param active: true gdy sensor aktywny,false gdy nieaktywny
		"""
		self.battery=battery
		self.sensing_range=sensing_range
		self.localization=localization
		self.active=True

