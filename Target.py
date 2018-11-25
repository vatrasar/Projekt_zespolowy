from graph import Node
class Target(Node):
	def __init__(self, localization):
		self.localization = localization
		super().__init__(0)

	def get_key(self):
		return (self.localization,super().get_key())

	def __hash__(self) -> int:
		return hash(self.get_key())

	def __eq__(self, obj) -> bool:
		return obj.localization==self.localization and super().__eq__()

