class Scheduler:

	def __init__(self,sensors_list,target_list,sensing_range, paint):
		"""
		:param sensors_list:lista obiektów typu Sensor
		:param sensing_range:
		:param targets_list:pytanie czy będziemy obserwować cele czy jakiś obszar
		jeśli obszar to parametr jest niepotrzebny
		:param duration: czas trwania symulacji (czas życia sieci sensorowej)
		:param paint: obiekt łączący z interfacem, uaktualnia ekran
		z symulacja, najlepiej użyj self.paint.paint(self)
		za każdym razem kiedy włączysz lub wyłączysz jakiś sensor,
		możesz też użyć tej funkcji np. w jakiejś głównej pętli symulacji
		:param percent_observed_targets: procent obserwowanych celów
		"""
		self.sensor_list=sensors_list
		self.target_list = target_list
		self.sensor_range=sensing_range
		self.duration = 0
		self.paint = paint
		self.percent_observed_targets = 0
	def get_sensor_list(self):
		pass
	def run(self):
		#Tu algorytm symulacji
		
		#Przykładowy kod prezentujący interface, musisz podać co najmniej
		#1000 sensorów. Przykładowe dane do przetestowania tego kodu
		#1000 sensorów, 1000 targetów, 10 zasięg, 10 bateria, 
		#1000 wysokość, 1000 szerokość
		i=0
		while i < 1000:
			self.paint.paint(self)
			self.sensor_list[i].active = False
			i+=1
