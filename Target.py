
class Target:
	def __init__(self, localization):
		self.localization = localization

	def get_key(self):
		return (self.localization)

	def __hash__(self) -> int:
		return hash(self.get_key())

	def __eq__(self, obj) -> bool:
		if obj.localization==self.localization:
			return True
		else:
			return False

