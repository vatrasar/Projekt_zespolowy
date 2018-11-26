from graph import Node
class Target(Node):
	def __init__(self, localization):
		self.localization = localization
		self.covering_sensors=[]
		super().__init__(0)

	def get_key(self):
		return (self.localization,super().get_key())

	def __hash__(self) -> int:
		return self.get_key().__hash__()

	def __eq__(self, obj) -> bool:
		return obj.localization==self.localization

