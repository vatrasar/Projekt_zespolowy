
class Target():
	def __init__(self, localization):
		self.localization = localization
		self.covering_sensors=[]


	def get_key(self):
		return self.localization

	def __hash__(self) -> int:
		return self.get_key().__hash__()

	def __eq__(self, obj) -> bool:
		return obj.localization==self.localization

