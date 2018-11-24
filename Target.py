
class Target:
	def __init__(self, localization):
		self.localization = localization
	def get_key(self):
		return (self.localization)
	def __hash__(self):
		return hash(self.get_key())

	def __eq__(self, o: object) -> bool:
		if object.localization==self.localization:
			return True
		else:
			return False

